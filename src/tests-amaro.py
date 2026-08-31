# -*- coding: utf-8 -*-
"""Controles du site AMARO, sur les pages rendues.

    python3 tests-amaro.py [port]

Ce fichier verifie LA PAGE, pas le generateur. Lire page_amaro.py ne dit pas
quelle regle CSS a gagne, si une image est cassee, ni si un formulaire a
vraiment refuse un champ vide — il faut le demander au navigateur.

Les controles qui comptent vraiment ici :

  - le 360 est verifie NUMERIQUEMENT, angle par angle, contre la projection
    d'un cylindre. Une rotation « qui a l'air de tourner » peut glisser du
    mauvais cote ou s'ecraser au mauvais moment, et l'oeil ne le voit pas ;
  - le compteur de champs vides est compare a ce que la page AFFICHE. Si un
    chiffre invente se glissait un jour dans une fiche, ce test tombe ;
  - le formulaire est SOUMIS. Un formulaire qui affiche « envoye » sans
    destinataire est le defaut le plus cher de la page, et il ne se voit pas
    en lisant le code ;
  - le contraste est mesure sur les couleurs CALCULEES. Une palette rose sur
    blanc passe presque partout et rate exactement aux endroits ou l'on a
    mis du rose clair sur du rose clair.
"""

import math
import os
import re
import sys

from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

import contenu as C                                          # noqa: E402
from bouteille import CX, Y_ETIQUETTE, rayon                 # noqa: E402
from page_amaro import PAGES                                 # noqa: E402

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8807
BASE = 'http://127.0.0.1:%d/' % PORT

OK, KO = [], []


def dit(bon, quoi, detail=''):
    (OK if bon else KO).append(quoi)
    print('%s %s%s' % ('  ok  ' if bon else '  KO  ', quoi,
                       ('  — ' + detail) if detail else ''))


# ---------------------------------------------------------------------------

def lum(c):
    """Luminance relative WCAG d'un « rgb(r, g, b) »."""
    n = [int(x) / 255.0 for x in re.findall(r'\d+', c)[:3]]
    n = [(v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4)
         for v in n]
    return 0.2126 * n[0] + 0.7152 * n[1] + 0.0722 * n[2]


def contraste(a, b):
    la, lb = lum(a), lum(b)
    if la < lb:
        la, lb = lb, la
    return (la + 0.05) / (lb + 0.05)


FOND_JS = """(el) => {
  // Le fond effectif : on remonte tant qu'il est transparent, sinon on
  // compare un texte a « rgba(0,0,0,0) » et tout passe.
  let n = el;
  while (n) {
    const c = getComputedStyle(n).backgroundColor;
    if (c && c !== 'rgba(0, 0, 0, 0)' && c !== 'transparent') return c;
    n = n.parentElement;
  }
  return 'rgb(255, 255, 255)';
}"""


def test_contraste(page, url):
    cibles = ('p, h1, h2, h3, h4, a, li, th, td, label, .vide, .eyebrow, '
              '.station__fleche, .btn')
    mauvais = []
    els = page.query_selector_all(cibles)
    for el in els[:220]:
        txt = (el.inner_text() or '').strip()
        if not txt or len(txt) > 400:
            continue
        if not el.is_visible():
            continue
        av = el.evaluate('(e) => getComputedStyle(e).color')
        ar = el.evaluate(FOND_JS)
        taille = float(el.evaluate(
            '(e) => parseFloat(getComputedStyle(e).fontSize)'))
        gras = el.evaluate(
            '(e) => parseInt(getComputedStyle(e).fontWeight) >= 600')
        seuil = 3.0 if (taille >= 24 or (taille >= 18.66 and gras)) else 4.5
        r = contraste(av, ar)
        if r < seuil:
            mauvais.append('%s « %s » %.2f < %.1f'
                           % (el.evaluate('(e) => e.tagName.toLowerCase()'),
                              txt[:38], r, seuil))
    dit(not mauvais, 'contraste — %s' % url,
        ' | '.join(mauvais[:3]) if mauvais else '%d éléments' % len(els))


def test_debordement(page, url):
    """Aucun debordement horizontal : c'est le defaut mobile numero un.

    Le VERDICT porte sur scrollWidth : c'est lui, et lui seul, qui dit si la
    page defile de cote. La liste d'elements n'est qu'un diagnostic, la pour
    expliquer POURQUOI.

    Premiere version : elle signalait aussi `left < 0`, et les quatorze pages
    tombaient sur le lien d'evitement, gare a `left:-9999px` — un idiome
    d'accessibilite, pas un debordement. Un element parti a gauche ne cree
    aucune barre de defilement en lecture gauche-a-droite ; seul ce qui
    depasse a DROITE en cree.
    """
    trop = page.evaluate("""() => {
      const w = document.documentElement.clientWidth, sortis = [];
      document.querySelectorAll('body *').forEach(e => {
        const r = e.getBoundingClientRect();
        if (r.width === 0 || r.height === 0) return;
        // Les conteneurs qui defilent d'eux-memes ont le droit de depasser.
        const st = getComputedStyle(e);
        if (st.overflowX === 'auto' || st.overflowX === 'scroll') return;
        if (r.right > w + 1.5) {
          sortis.push(e.tagName.toLowerCase() + '.' +
                      (e.className.toString().split(' ')[0] || '?') +
                      ' [' + Math.round(r.left) + '..' + Math.round(r.right) + ']');
        }
      });
      return sortis.slice(0, 5);
    }""")
    ecart = page.evaluate(
        '() => document.documentElement.scrollWidth '
        '- document.documentElement.clientWidth')
    dit(ecart <= 1, 'pas de débordement horizontal — %s' % url,
        ('%d px de trop | ' % ecart if ecart > 1 else '') + ' | '.join(trop))


def test_images(page, url):
    """Aucune image cassee, dans le viewport uniquement.

    Chercher hors viewport ferait echouer tout ce qui est en chargement
    differe : l'image n'est pas cassee, elle n'est pas encore demandee.
    """
    casse = page.evaluate("""() => {
      const out = [];
      document.querySelectorAll('img').forEach(i => {
        const r = i.getBoundingClientRect();
        if (r.bottom < 0 || r.top > innerHeight) return;
        if (!i.complete || i.naturalWidth === 0) out.push(i.src);
      });
      return out;
    }""")
    # Les bouteilles sont des SVG : une reference cassee donne un `use` qui
    # ne dessine rien. On verifie que le corps existe et a une aire.
    svg_ok = page.evaluate("""() => {
      const u = document.querySelector('svg.bouteille use[href="#amaro-corps"]');
      if (!u) return true;   // page sans bouteille
      const b = u.getBoundingClientRect();
      return b.width > 10 && b.height > 40;
    }""")
    dit(not casse and svg_ok, 'aucune image cassée — %s' % url,
        ' | '.join(casse[:3]) or ('' if svg_ok else 'use #amaro-corps vide'))


def test_langue(page, url):
    """Passer en anglais ne doit laisser aucun texte francais visible."""
    page.click('[data-langue="en"]')
    page.wait_for_timeout(200)
    restes = page.evaluate("""() => {
      const out = [];
      document.querySelectorAll('[data-fr][data-en]').forEach(e => {
        const en = e.getAttribute('data-en');
        if (en === null || en === '') return;
        if (e.textContent.trim() === e.getAttribute('data-fr').trim()
            && en.trim() !== e.getAttribute('data-fr').trim()) {
          out.push(e.textContent.trim().slice(0, 40));
        }
      });
      return out.slice(0, 5);
    }""")
    lang = page.evaluate('() => document.documentElement.lang')
    page.click('[data-langue="fr"]')
    page.wait_for_timeout(150)
    dit(not restes and lang == 'en', 'bascule FR→EN — %s' % url,
        ' | '.join(restes))


# ---------------------------------------------------------------------------
# Le 360, verifie contre la geometrie et non contre l'impression
# ---------------------------------------------------------------------------

def test_360(page):
    R = rayon((Y_ETIQUETTE[0] + Y_ETIQUETTE[1]) / 2.0)
    erreurs = []
    for deg in (0, 30, 60, 89, 91, 120, 180, 240, 300, 359):
        page.evaluate("""(d) => {
          const c = document.getElementById('curseur-angle');
          c.value = d;
          c.dispatchEvent(new Event('input', {bubbles: true}));
        }""", deg)
        page.wait_for_timeout(40)
        a = math.radians(deg)
        etat = page.evaluate("""() => {
          const g = (id) => {
            const e = document.getElementById(id);
            return {t: e.getAttribute('transform'),
                    o: parseFloat(e.getAttribute('opacity'))};
          };
          return {face: g('b-v360-i-face'), dos: g('b-v360-i-dos'),
                  cd: g('b-v360-i-couture-d'), cg: g('b-v360-i-couture-g'),
                  lu: document.getElementById('lecture-angle').textContent};
        }""")

        def lire(t):
            m = re.match(r'translate\(([-\d.e]+),0\) scale\(([-\d.e]+),1\)', t)
            return (float(m.group(1)), float(m.group(2))) if m else (None, None)

        # ── L'etiquette de face, azimut 0 : x = CX + R sin(a), largeur cos(a)
        c, s = math.cos(a), math.sin(a)
        if c > 0.02:
            tx, sx = lire(etat['face']['t'])
            if tx is None or abs(tx - (CX + R * s)) > 0.6:
                erreurs.append('%d° face x=%s attendu %.1f'
                               % (deg, tx, CX + R * s))
            if sx is None or abs(sx - c) > 0.01:
                erreurs.append('%d° face échelle=%s attendu %.3f' % (deg, sx, c))
            if etat['face']['o'] <= 0:
                erreurs.append('%d° face invisible alors que cos>0' % deg)
        elif etat['face']['o'] > 0:
            erreurs.append('%d° face visible alors que cos<=0' % deg)

        # ── Le panneau arriere, azimut pi : visible exactement quand cos(a)<0
        dos_visible = etat['dos']['o'] > 0
        if dos_visible != (math.cos(a + math.pi) > 0.02):
            erreurs.append('%d° dos visible=%s (cos(a+pi)=%.3f)'
                           % (deg, dos_visible, math.cos(a + math.pi)))
        if dos_visible:
            tx, sx = lire(etat['dos']['t'])
            attendu = CX + R * math.sin(a + math.pi)
            if tx is None or abs(tx - attendu) > 0.6:
                erreurs.append('%d° dos x=%s attendu %.1f' % (deg, tx, attendu))

        # ── Les coutures : ecrasement sin(t), visibles si cos(t) > 0
        for nom, az in (('cd', math.pi / 2), ('cg', -math.pi / 2)):
            vis = etat[nom]['o'] > 0
            if vis != (math.cos(a + az) > 0):
                erreurs.append('%d° %s visible=%s (cos=%.3f)'
                               % (deg, nom, vis, math.cos(a + az)))
            if vis:
                _, sx = lire(etat[nom]['t'])
                att = math.sin(a + az)
                if sx is None or abs(sx - att) > 0.01:
                    erreurs.append('%d° %s échelle=%s attendu %.3f'
                                   % (deg, nom, sx, att))

        if etat['lu'].rstrip('°') != str(deg):
            erreurs.append('%d° lecture affiche « %s »' % (deg, etat['lu']))

    dit(not erreurs, '360° — projection du cylindre exacte',
        ' | '.join(erreurs[:4]) or '10 angles')

    # Le glissement a la souris doit ecrire le MEME etat que le curseur.
    boite = page.query_selector('svg.bouteille').bounding_box()
    page.mouse.move(boite['x'] + boite['width'] / 2,
                    boite['y'] + boite['height'] / 2)
    page.mouse.down()
    page.mouse.move(boite['x'] + boite['width'] / 2 + 120,
                    boite['y'] + boite['height'] / 2, steps=6)
    page.mouse.up()
    page.wait_for_timeout(80)
    ang = page.evaluate(
        '() => parseInt(document.getElementById("curseur-angle").value)')
    dit(ang != 0, '360° — le glissement écrit le même état que le curseur',
        'angle après glissement : %d°' % ang)


# ---------------------------------------------------------------------------
# Les champs vides : la page doit dire exactement ce que contenu.py dit
# ---------------------------------------------------------------------------

def test_champs_vides(nav):
    # On compare les CLES DISTINCTES, pas le nombre de pastilles.
    #
    # Premiere version : elle comparait un total. Il valait 113 pour 45 champs
    # declares, et le test criait au mensonge alors que le site etait juste —
    # la fiche saveur est rendue huit fois, la fiche eau deux fois. Compter
    # des rendus quand on veut verifier des declarations, c'est mesurer autre
    # chose que ce qu'on croit mesurer.
    attendus = set(t['cle'] for t in C.champs_vides())
    attendus |= set('reseau-' + c for c, _, _ in C.RESEAUX)
    vues = set()
    faux = []
    ctx = nav.new_context(viewport={'width': 1280, 'height': 900})
    page = ctx.new_page()
    for nom, _ in PAGES:
        page.goto(BASE + nom, wait_until='networkidle')
        n = page.evaluate("""() => {
          const out = [];
          document.querySelectorAll('[data-vide]').forEach(e => {
            out.push([e.getAttribute('data-vide'), e.textContent.trim()]);
          });
          return out;
        }""")
        for cle, txt in n:
            vues.add(cle)
            if txt not in ('à renseigner', 'to be provided'):
                faux.append('%s / %s : « %s »' % (nom, cle, txt))
    ctx.close()
    manquants = sorted(attendus - vues)
    en_trop = sorted(vues - attendus)
    dit(not manquants and not en_trop,
        'champs vides — la page affiche exactement ce que contenu.py déclare',
        'absents de la page : %s | en trop : %s'
        % (manquants[:3], en_trop[:3]) if (manquants or en_trop)
        else '%d clés distinctes' % len(vues))
    dit(not faux, 'aucun champ vide rempli par une valeur inventée',
        ' | '.join(faux[:3]))


# ---------------------------------------------------------------------------
# Le formulaire B2B, soumis pour de vrai
# ---------------------------------------------------------------------------

def test_formulaire(page):
    page.goto(BASE + 'business.html', wait_until='networkidle')
    page.click('#b2b button[type="submit"]')
    page.wait_for_timeout(200)
    erreurs = page.evaluate("""() => {
      const o = [];
      document.querySelectorAll('.champ__err').forEach(p => {
        if (p.textContent.trim()) o.push(p.id);
      });
      return o;
    }""")
    # societe, pays, ville, contact, courriel, marches + secteur + consentement
    dit(len(erreurs) >= 8, 'formulaire vide — refusé, champ par champ',
        '%d messages : %s' % (len(erreurs), ', '.join(erreurs[:4])))
    montre = page.evaluate(
        '() => !document.getElementById("resultat").hidden')
    dit(not montre, 'formulaire vide — aucun accusé de réception affiché')

    # Courriel malforme
    for champ, val in (('societe', 'Test SARL'), ('pays', 'Canada'),
                       ('ville', 'Montréal'), ('contact', 'A. Talmale'),
                       ('courriel', 'pas-une-adresse'),
                       ('marches', 'Québec, Ontario')):
        page.fill('#f-' + champ, val)
    page.check('#secteurs input[value="distributeur"]')
    page.check('#f-consentement')
    page.click('#b2b button[type="submit"]')
    page.wait_for_timeout(200)
    err_mail = page.inner_text('#e-courriel').strip()
    dit(bool(err_mail), 'courriel malformé — refusé', err_mail)

    page.fill('#f-courriel', 'contact@exemple.com')
    page.click('#b2b button[type="submit"]')
    page.wait_for_timeout(250)
    res = page.inner_text('#resultat').strip()
    visible = page.evaluate(
        '() => !document.getElementById("resultat").hidden')
    # Ce qu'on cherche, c'est une AFFIRMATION d'envoi, pas le mot « envoye ».
    # Premiere version : le motif \benvoyé attrapait « Rien n'a été envoyé »,
    # c'est-a-dire exactement la phrase qui prouve que le panneau est honnete.
    # Un test qui echoue sur la bonne reponse est un test qui apprend a
    # supprimer la bonne reponse.
    ment = re.search(
        r"(?<!n’a été )(?<!n'a été )\b(demande envoyée|message envoyé|"
        r"votre demande a bien|merci de votre demande|has been sent|"
        r"was sent|we will get back|thank you for your enquiry)\b",
        res, re.I)
    dit(visible and not ment,
        'formulaire valide — dit ce qui partirait, jamais « envoyé »',
        res.replace('\n', ' ')[:90])
    dit('societe : Test SARL' in res,
        'formulaire valide — les valeurs saisies sont montrées telles quelles')


# ---------------------------------------------------------------------------
# Filtres du catalogue
# ---------------------------------------------------------------------------

def test_filtres(page):
    page.goto(BASE + 'produits.html', wait_until='networkidle')
    total = len(C.EAUX) + len(C.SAVEURS)
    cas = [('tous', total), ('plate', 1), ('gazeuse', 1),
           ('aromatisee', len(C.SAVEURS))]
    mauvais = []
    for val, attendu in cas:
        page.check('#filtres input[value="%s"]' % val)
        page.wait_for_timeout(120)
        n = page.evaluate(
            '() => document.querySelectorAll("#produits .produit:not([hidden])")'
            '.length')
        if n != attendu:
            mauvais.append('%s : %d au lieu de %d' % (val, n, attendu))
        lu = page.inner_text('#compte-produits')
        if not lu.startswith(str(n)):
            mauvais.append('%s : compteur « %s » pour %d visibles'
                           % (val, lu, n))
    dit(not mauvais, 'filtres du catalogue — le compteur suit l’affichage',
        ' | '.join(mauvais))


# ---------------------------------------------------------------------------
# Sans JavaScript : rien ne doit disparaitre
# ---------------------------------------------------------------------------

def test_sans_js(nav):
    ctx = nav.new_context(viewport={'width': 1280, 'height': 900},
                          java_script_enabled=False)
    page = ctx.new_page()
    manques = []
    for nom, _ in PAGES:
        page.goto(BASE + nom, wait_until='domcontentloaded')
        vu = page.evaluate  # indisponible sans JS : on mesure autrement
        txt = page.inner_text('main').strip()
        if len(txt) < 200:
            manques.append('%s : %d caractères visibles' % (nom, len(txt)))
    # Le catalogue doit montrer TOUS les produits sans script.
    page.goto(BASE + 'produits.html', wait_until='domcontentloaded')
    n = len(page.query_selector_all('#produits .produit'))
    caches = len(page.query_selector_all('#produits .produit[hidden]'))
    ctx.close()
    dit(not manques, 'sans JavaScript — aucune page ne se vide',
        ' | '.join(manques[:3]))
    dit(caches == 0 and n == len(C.EAUX) + len(C.SAVEURS),
        'sans JavaScript — le catalogue reste complet',
        '%d produits, %d masqués' % (n, caches))


# ---------------------------------------------------------------------------
# Liens
# ---------------------------------------------------------------------------

def test_liens(page):
    page.goto(BASE + 'index.html', wait_until='networkidle')
    hrefs = page.evaluate("""() => {
      const s = new Set();
      document.querySelectorAll('a[href]').forEach(a => {
        const h = a.getAttribute('href');
        if (h && !h.startsWith('#') && !h.startsWith('http')) s.add(h);
      });
      return [...s];
    }""")
    morts = [h for h in hrefs
             if not os.path.isfile(os.path.join(ICI, 'demo', h.split('#')[0]))]
    dit(not morts, 'liens internes — tous résolus',
        '%d liens, morts : %s' % (len(hrefs), morts[:3]))


# ---------------------------------------------------------------------------

def main():
    largeurs = [('bureau', 1280, 900), ('mobile', 390, 780)]
    with sync_playwright() as p:
        nav = p.chromium.launch(args=['--disable-lcd-text',
                                      '--force-color-profile=srgb'])
        for etiquette, w, h in largeurs:
            print('\n── %s %dx%d ' % (etiquette, w, h) + '─' * 40)
            ctx = nav.new_context(viewport={'width': w, 'height': h},
                                  is_mobile=(w < 500))
            page = ctx.new_page()
            for nom, _ in PAGES:
                page.goto(BASE + nom, wait_until='networkidle')
                page.wait_for_timeout(150)
                test_debordement(page, '%s (%s)' % (nom, etiquette))
                test_images(page, '%s (%s)' % (nom, etiquette))
                if etiquette == 'bureau':
                    test_contraste(page, nom)
                    test_langue(page, nom)
            ctx.close()

        print('\n── fonctionnel ' + '─' * 44)
        ctx = nav.new_context(viewport={'width': 1400, 'height': 950})
        page = ctx.new_page()
        page.goto(BASE + 'bouteille.html', wait_until='networkidle')
        test_360(page)
        test_formulaire(page)
        test_filtres(page)
        test_liens(page)
        ctx.close()

        test_champs_vides(nav)
        test_sans_js(nav)
        nav.close()

    print('\n' + '=' * 60)
    print('%d contrôles passés, %d échoués' % (len(OK), len(KO)))
    for k in KO:
        print('   KO : %s' % k)
    return 1 if KO else 0


if __name__ == '__main__':
    raise SystemExit(main())
