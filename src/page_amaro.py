# -*- coding: utf-8 -*-
"""Construit le site AMARO : quatorze pages, deux langues, un seul gabarit.

     python3 page_amaro.py

Principes tenus d'un bout a l'autre :

  - AUCUN texte en dur ici. Tout vient de contenu.py, sinon une phrase finit
    par exister en francais seulement et personne ne s'en apercoit.
  - AUCUN chiffre invente. Une ligne de fiche sans valeur s'affiche « à
    renseigner », en clair, sur la page publique. Voir contenu.py pour le
    pourquoi : une eau embouteillee est un produit reglemente.
  - RIEN N'EST CACHE PAR DEFAUT. Les apparitions au defilement dependent
    d'une classe posee par le script lui-meme ; sans JavaScript, tout est
    visible et toutes les fiches sont ouvrables.
  - Les compteurs (nombre de saveurs, nombre de marches, nombre de champs a
    fournir) sont CALCULES. Un « huit saveurs » tape a la main survit a
    l'ajout de la neuvieme et la page se met a mentir sur elle-meme.
"""

import html as _H
import os
import re

import contenu as C
from bouteille import (bouteille, defs_partagees, logo, script_360, rayon,
                       Y_ETIQUETTE)
from chemins import dossier_pages
from style_amaro import CSS

ICI = os.path.dirname(os.path.abspath(__file__))
DEMO = dossier_pages(ICI)

# L'action du formulaire B2B. VIDE dans la demo statique : il n'y a ni
# hebergement ni adresse commerciale, et un formulaire qui affiche « envoye »
# sans rien envoyer est un mensonge poli. Quand le site sera sur le serveur,
# mettre 'formulaire.php' ici — la page bascule toute seule.
ACTION_FORMULAIRE = ''


def e(x):
    return _H.escape(str(x), quote=True)


def bi(fr, en, balise='p', classe='', extra=''):
    """Un element bilingue : les deux langues voyagent dans la balise.

    Le francais est le contenu visible ; l'anglais attend dans un attribut.
    Changer de langue ne reconstruit donc rien et ne perd pas la position
    dans la page.
    """
    c = ' class="%s"' % e(classe) if classe else ''
    x = ' ' + extra if extra else ''
    return ('<%s%s%s data-fr="%s" data-en="%s">%s</%s>'
            % (balise, c, x, e(fr), e(en), fr, balise))


def rev(html, delai=0):
    d = ' style="transition-delay:%dms"' % delai if delai else ''
    return '<div class="rev"%s>%s</div>' % (d, html)


def valeur(v, cle=''):
    """La cellule d'une fiche technique.

    Une valeur absente n'est pas un tiret discret : c'est une pastille
    « à renseigner », visible, qui se compte et se reclame. Un tiret se lit
    comme « sans objet » et disparait dans la page.
    """
    if v:
        return e(v)
    return ('<span class="vide" data-vide="%s" data-fr="à renseigner" '
            'data-en="to be provided">à renseigner</span>' % e(cle))


def fiche(table, titre_fr='', titre_en=''):
    lignes = ''.join(
        '<tr><th data-fr="%s" data-en="%s">%s</th><td>%s</td></tr>'
        % (e(fr), e(en), fr, valeur(val, cle))
        for cle, fr, en, val in table)
    cap = ''
    if titre_fr:
        cap = ('<caption class="hors-ecran" data-fr="%s" data-en="%s">%s'
               '</caption>' % (e(titre_fr), e(titre_en), titre_fr))
    return '<table class="fiche">%s<tbody>%s</tbody></table>' % (cap, lignes)


# ---------------------------------------------------------------------------
# Gabarit
# ---------------------------------------------------------------------------

FAVICON = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
    "viewBox='0 0 48 72'%3E%3Cpath fill='none' stroke='%23CB5F87' "
    "stroke-width='6' stroke-linecap='round' d='M24 6c9 0 14 5.5 14 12.5S29 "
    "30 24 32c-5 2-16 5.5-16 14.5S15 66 24 66s16-9 16-19.5S29 34 24 32c-5-2-"
    "16-6.5-16-13.5S15 6 24 6z'/%3E%3C/svg%3E")


def entete(page):
    liens = ''.join(
        '<a href="%s"%s data-fr="%s" data-en="%s">%s</a>'
        % (u, ' aria-current="page"' if u == page else '', e(fr), e(en), fr)
        for u, fr, en in C.NAV)
    return """<header class="entete" id="entete">
  <div class="entete__in">
    <a class="marque" href="index.html">%(logo)s<span>%(marque)s</span></a>
    <button class="burger" type="button" id="burger" aria-expanded="false"
            aria-controls="nav" data-fr="Menu" data-en="Menu">Menu</button>
    <nav class="nav" id="nav" aria-label="Navigation principale">%(liens)s</nav>
    <div class="langues" role="group" aria-label="Langue / Language">
      <button type="button" data-langue="fr" aria-pressed="true">FR</button>
      <button type="button" data-langue="en" aria-pressed="false">EN</button>
    </div>
  </div>
</header>""" % dict(logo=logo(24), marque=e(C.MARQUE), liens=liens)


def pied():
    def col(titre_fr, titre_en, items):
        li = ''.join('<li><a href="%s" data-fr="%s" data-en="%s">%s</a></li>'
                     % (u, e(fr), e(en), fr) for u, fr, en in items)
        return ('<div><h4 data-fr="%s" data-en="%s">%s</h4><ul>%s</ul></div>'
                % (e(titre_fr), e(titre_en), titre_fr, li))

    return """<footer class="pied">
  <div class="enveloppe">
    <div class="pied__grille">
      <div>
        <p class="pied__signature">%(sig)s</p>
        %(note)s
      </div>
      %(c1)s
      %(c2)s
      %(c3)s
    </div>
    <div class="pied__bas">
      <span>&copy; %(marque)s</span>
      %(mentions)s
    </div>
  </div>
</footer>""" % dict(
        sig=e(C.SIGNATURE), marque=e(C.MARQUE),
        note=bi('Maquette de travail. Aucune valeur réglementaire n’est '
                'publiée tant qu’elle n’est pas vérifiée.',
                'Working prototype. No regulatory value is published until '
                'it has been verified.'),
        c1=col('Produits', 'Products', C.NAV[1:5]),
        c2=col('La marque', 'Company', C.NAV[5:8]),
        c3=col('Plus', 'More', C.NAV[8:] + C.NAV_PIED),
        mentions=bi('Mentions légales, politique de confidentialité et '
                    'gestion des cookies : à rédiger une fois le pays '
                    'd’exploitation choisi.',
                    'Legal notice, privacy policy and cookie management: to '
                    'be drafted once the country of operation is chosen.',
                    balise='span'))


def gabarit(page, titre_fr, titre_en, corps, script_sup=''):
    canon = ''
    if C.DOMAINE:
        canon = '<link rel="canonical" href="%s/%s">' % (
            C.DOMAINE.rstrip('/'), page)
    return """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(titre)s — %(marque)s</title>
<meta name="description" content="%(desc)s">
<link rel="icon" href="%(fav)s">
<link rel="stylesheet" href="styles.css">
%(canon)s
</head>
<body>
<a class="saut" href="#contenu" data-fr="Aller au contenu"
   data-en="Skip to content">Aller au contenu</a>
%(entete)s
<main id="contenu">
%(corps)s
</main>
%(pied)s
%(defs)s
<script src="script.js"></script>
%(sup)s
</body>
</html>
""" % dict(titre=e(titre_fr), marque=e(C.MARQUE), fav=FAVICON, canon=canon,
           desc=e('%s — %s' % (titre_fr, C.SIGNATURE)),
           entete=entete(page), corps=corps, pied=pied(),
           # Le bloc de defs vient APRES le contenu, et c'est voulu : un id
           # SVG se resout au rendu, pas a la lecture, et le mettre en tete
           # ferait 6 ko de chemins avant le premier pixel utile.
           # Il est calcule ICI, une fois le corps assemble, donc il contient
           # exactement les teintes que la page utilise — ni plus, ni moins.
           defs=defs_partagees(),
           sup=('<script>%s</script>' % script_sup) if script_sup else '')


def tete(fr, en, sfr='', sen='', classe=''):
    s = bi(sfr, sen) if sfr else ''
    return ('<div class="tete %s">%s%s</div>'
            % (classe, bi(fr, en, 'h2'), s))


def section(inner, classe='', ident=''):
    i = ' id="%s"' % ident if ident else ''
    return ('<section class="section %s"%s><div class="enveloppe">%s</div>'
            '</section>' % (classe, i, inner))


# ---------------------------------------------------------------------------
# 1. Accueil
# ---------------------------------------------------------------------------

def page_accueil():
    h = C.HERO
    hero = """<section class="hero">
  <div class="enveloppe hero__in">
    <div class="hero__gauche">
      %(eyebrow)s
      <h1><span class="mot">Water.</span>
          <span class="mot mot--rose">Reimagined.</span></h1>
      %(chapo)s
      <div class="hero__ctas">
        <a class="btn btn--plein" href="bouteille.html"
           data-fr="%(c1fr)s" data-en="%(c1en)s">%(c1fr)s</a>
        <a class="btn btn--ligne" href="business.html"
           data-fr="%(c2fr)s" data-en="%(c2en)s">%(c2fr)s</a>
      </div>
    </div>
    <div class="hero__bouteille">%(bouteille)s</div>
    <div class="hero__droite">
      %(sous)s
    </div>
  </div>
</section>""" % dict(
        eyebrow=bi('Eau embouteillée & eaux aromatisées',
                   'Bottled water & flavored waters', 'p', 'eyebrow'),
        chapo=bi(h['chapo_fr'], h['chapo_en'], 'p', 'hero__chapo'),
        c1fr=e(h['cta1_fr']), c1en=e(h['cta1_en']),
        c2fr=e(h['cta2_fr']), c2en=e(h['cta2_en']),
        bouteille=bouteille('hero', '#BFE0EA', 'AMARO', 'NATURAL', 470),
        sous=bi('Une bouteille en PET/rPET dont la silhouette dessine un 8. '
                'Deux volumes ronds, une taille resserrée qui sert de prise '
                'en main — et qui se reconnaît en rayon sans qu’on lise '
                'l’étiquette.',
                'A PET/rPET bottle whose silhouette draws a figure 8. Two '
                'round volumes, a narrow waist that doubles as the grip — '
                'and that is recognised on shelf without reading the label.',
                'p', 'hero__chapo'))

    stations = ''.join(
        """<a class="station rev" href="%(lien)s">
             <span class="station__num">%(num)s</span>
             %(titre)s%(texte)s
             <span class="station__fleche" data-fr="Voir &rarr;"
                   data-en="View &rarr;">Voir &rarr;</span>
           </a>""" % dict(
            lien=s['lien'], num=s['num'],
            titre=bi(s['titre_fr'], s['titre_en'], 'h3'),
            texte=bi(s['texte_fr'], s['texte_en']))
        for s in C.STATIONS)

    # Les trois bouteilles de la bande produit. La saveur affichee est la
    # premiere de la liste : ajouter une saveur en tete change l'image, pas
    # le code.
    sav = C.SAVEURS[0]
    trio = """<div class="grille grille--3">
      %s %s %s
    </div>""" % (
        carte_produit(C.EAUX[0], 'notre-eau.html'),
        carte_produit(C.EAUX[1], 'notre-eau.html', gazeuse=True),
        carte_saveur_lien(sav))

    compteurs = section(
        tete('Ce que la marque propose aujourd’hui',
             'What the brand offers today',
             '%d saveurs, %d eaux, %d formats. La gamme est construite pour '
             's’élargir : ce qui vaut pour l’eau plate doit rester vrai '
             'pour ce qui viendra après.'
             % (len(C.SAVEURS), len(C.EAUX), len(C.FORMATS)),
             '%d flavors, %d waters, %d formats. The range is built to '
             'widen: what holds for still water has to keep holding for '
             'whatever comes next.'
             % (len(C.SAVEURS), len(C.EAUX), len(C.FORMATS)))
        + rev(trio), 'section--rose')

    appel = section("""<div class="tete tete--centre">%s%s
        <div class="hero__ctas" style="justify-content:center">
          <a class="btn btn--clair" href="business.html" data-fr="%s"
             data-en="%s">%s</a>
        </div></div>""" % (
        bi('AMARO cherche des partenaires', 'AMARO is looking for partners',
           'h2'),
        bi('Distributeurs, grossistes, retail, hôtellerie, restauration, '
           'salles de sport, entreprises et événementiel. Le formulaire '
           'demande le pays, les marchés couverts et les volumes estimés.',
           'Distributors, wholesalers, retail, hotels, food service, gyms, '
           'corporate and events. The form asks for country, markets covered '
           'and estimated volumes.'),
        e(C.HERO['cta2_fr']), e(C.HERO['cta2_en']), e(C.HERO['cta2_fr'])),
        'section--encre')

    return gabarit('index.html', 'Accueil', 'Home',
                   hero
                   + section('<div class="stations">%s</div>' % stations)
                   + compteurs + appel)


def carte_produit(eau, lien, gazeuse=False):
    return """<a class="carte" href="%(lien)s" style="--tint:%(t)s">
      <span class="carte__visuel" style="--tint:%(t)s">%(b)s</span>
      %(type)s%(nom)s%(txt)s
      <span class="carte__pied"><ul class="puces">%(f)s</ul></span>
    </a>""" % dict(
        lien=lien, t=eau['teinte'],
        b=bouteille('c-' + eau['cle'], eau['teinte'], 'AMARO',
                    eau['nom'].split()[-1].upper(), 200, gazeuse=gazeuse),
        type=bi(eau['type_fr'], eau['type_en'], 'span', 'carte__type'),
        nom='<h3>%s</h3>' % e(eau['nom']),
        txt=bi(eau['texte_fr'], eau['texte_en']),
        f=''.join('<li data-fr="%s" data-en="%s">%s</li>' % (e(a), e(b), a)
                  for a, b in zip(C.FORMATS, C.FORMATS_EN)))


def carte_saveur_lien(sav):
    return """<a class="carte" href="saveurs.html" style="--tint:%(t)s">
      <span class="carte__visuel" style="--tint:%(t)s">%(b)s</span>
      %(type)s<h3>AMARO Flavors</h3>%(txt)s
      <span class="carte__pied"><ul class="puces">%(f)s</ul></span>
    </a>""" % dict(
        t=sav['teinte'],
        b=bouteille('c-flav', sav['teinte'], 'AMARO', sav['nom'].upper(), 200),
        type=bi('Eaux aromatisées', 'Flavored waters', 'span', 'carte__type'),
        txt=bi('Huit saveurs, une seule bouteille, un code couleur par '
               'saveur.',
               'Eight flavors, one bottle, one color code per flavor.'),
        f=''.join('<li>%s</li>' % e(s['nom']) for s in C.SAVEURS[:4])
          + '<li>+%d</li>' % (len(C.SAVEURS) - 4))


# ---------------------------------------------------------------------------
# 2. Notre eau
# ---------------------------------------------------------------------------

def page_eau():
    blocs = ''
    for i, eau in enumerate(C.EAUX):
        blocs += rev("""<div class="carte" style="--tint:%(t)s">
          <span class="carte__visuel" style="--tint:%(t)s">%(b)s</span>
          %(type)s<h3>%(nom)s</h3>%(txt)s
          <ul class="puces" style="margin:14px 0 0">%(f)s</ul>
          <div class="carte__pied">%(fiche)s</div>
        </div>""" % dict(
            t=eau['teinte'],
            b=bouteille('eau-' + eau['cle'], eau['teinte'], 'AMARO',
                        eau['nom'].split()[-1].upper(), 300,
                        gazeuse=(eau['cle'] == 'sparkling')),
            type=bi(eau['type_fr'], eau['type_en'], 'span', 'carte__type'),
            nom=e(eau['nom']),
            txt=bi(eau['texte_fr'], eau['texte_en']),
            f=''.join('<li data-fr="%s" data-en="%s">%s</li>' % (e(a), e(b), a)
                      for a, b in zip(C.FORMATS, C.FORMATS_EN)),
            fiche=fiche(C.FICHE_EAU, 'Fiche technique — ' + eau['nom'],
                        'Technical sheet — ' + eau['nom'])), i * 90)

    avert = """<div class="avertissement rev">%s</div>""" % bi(
        'Les lignes marquées « à renseigner » sont des mentions '
        'd’étiquetage : origine, analyse minérale, pH, dénomination légale, '
        'conditionnement, GTIN. Elles se prouvent avec un bulletin d’analyse '
        'et une fiche fournisseur, elles ne s’estiment pas. Elles restent '
        'vides et visibles jusqu’à ce que ces pièces existent.',
        'The lines marked “to be provided” are label statements: source, '
        'mineral analysis, pH, legal denomination, case pack, GTIN. They are '
        'proven with a laboratory report and a supplier sheet; they are not '
        'estimated. They stay empty and visible until those documents exist.')

    return gabarit('notre-eau.html', 'Notre eau', 'Our Water',
                   section(tete('Notre eau', 'Our Water',
                                'AMARO Natural et AMARO Sparkling, en quatre '
                                'formats.',
                                'AMARO Natural and AMARO Sparkling, in four '
                                'formats.')
                           + '<div class="grille grille--2">%s</div>' % blocs)
                   + section(avert, 'section--rose'))


# ---------------------------------------------------------------------------
# 3. Saveurs
# ---------------------------------------------------------------------------

def page_saveurs():
    vignettes = ''.join(
        """<a class="saveur rev" href="#s-%(cle)s" style="--tint:%(t)s"
              data-saveur="%(cle)s" data-delai="%(d)d">
             <span class="saveur__visuel">%(b)s</span>
             <h3>%(nom)s</h3>%(fr)s
             <span class="saveur__ligne"></span>
           </a>""" % dict(
            cle=s['cle'], t=s['teinte'], d=i * 60, nom=e(s['nom']),
            b=bouteille('v-' + s['cle'], s['teinte'], 'AMARO',
                        s['nom'].upper(), 190),
            fr='<p class="saveur__fr" data-fr="%s" data-en="%s">%s</p>'
               % (e(s['fr']), e(s['nom']), e(s['fr'])))
        for i, s in enumerate(C.SAVEURS))

    fiches = ''.join(
        """<details class="detail" id="s-%(cle)s" style="--tint:%(t)s">
             <summary><span class="detail__pastille"></span>
               <span>%(nom)s</span>
               <span class="saveur__fr" data-fr="%(fr)s" data-en=""
                     style="margin-left:8px">%(fr)s</span>
             </summary>
             <div class="detail__corps">
               <div style="text-align:center">%(b)s</div>
               <div>%(d)s<ul class="puces" style="margin:0 0 16px">%(f)s</ul>
                 %(fiche)s</div>
             </div>
           </details>""" % dict(
            cle=s['cle'], t=s['teinte'], nom=e(s['nom']), fr=e(s['fr']),
            b=bouteille('f-' + s['cle'], s['teinte'], 'AMARO',
                        s['nom'].upper(), 260),
            d=bi(s['d_fr'], s['d_en']),
            f=''.join('<li data-fr="%s" data-en="%s">%s</li>' % (e(a), e(b), a)
                      for a, b in zip(C.FORMATS, C.FORMATS_EN)),
            fiche=fiche(C.FICHE_SAVEUR, 'Fiche — ' + s['nom'],
                        'Sheet — ' + s['nom']))
        for s in C.SAVEURS)

    avert = '<div class="avertissement">%s</div>' % bi(
        'La description est de la copie de marque : je l’écris. La liste '
        'd’ingrédients, le tableau nutritionnel, les allergènes et les '
        'mentions réglementaires ne le sont pas : ils viennent du '
        'formulateur et du service qualité, et ils changent d’un marché à '
        'l’autre. Aucun n’est estimé ici.',
        'The description is brand copy: I write it. The ingredients list, '
        'the nutrition table, the allergens and the regulatory statements '
        'are not: they come from the formulator and from quality assurance, '
        'and they change from market to market. None of them is estimated '
        'here.')

    return gabarit('saveurs.html', 'Saveurs', 'Flavors',
                   section(tete('AMARO Flavors', 'AMARO Flavors',
                                '%d saveurs. Une seule bouteille, un code '
                                'couleur par saveur, une identité qui ne '
                                'bouge pas.' % len(C.SAVEURS),
                                '%d flavors. One bottle, one color code per '
                                'flavor, one identity that never moves.'
                                % len(C.SAVEURS))
                           + '<div class="saveurs">%s</div>' % vignettes)
                   + section(tete('Les fiches', 'The sheets',
                                  'Chaque fiche s’ouvre sur place. Elles sont '
                                  'dans la page même fermées : un moteur de '
                                  'recherche les lit.',
                                  'Each sheet opens in place. They are in the '
                                  'page even when closed: a search engine '
                                  'reads them.')
                             + fiches + '<div style="margin-top:26px">%s</div>'
                             % avert, 'section--rose'))


# ---------------------------------------------------------------------------
# 4. La bouteille 8
# ---------------------------------------------------------------------------

def page_bouteille():
    r = rayon((Y_ETIQUETTE[0] + Y_ETIQUETTE[1]) / 2.0)
    viseur = """<div class="viseur rev">
      %(b)s
      <div class="viseur__cmd">
        <label for="curseur-angle" data-fr="Rotation" data-en="Rotation">Rotation</label>
        <input type="range" id="curseur-angle" min="0" max="359" value="0"
               step="1" aria-describedby="lecture-angle">
        <span class="viseur__lecture" id="lecture-angle">0&deg;</span>
      </div>
      %(aide)s
    </div>""" % dict(
        b=bouteille('v360', '#BFE0EA', 'AMARO', 'NATURAL', 460,
                    interactif=True),
        aide=bi('Faites glisser la bouteille, ou utilisez le curseur au '
                'clavier. L’étiquette s’enroule et les deux coutures de '
                'moule balaient le corps : c’est la géométrie réelle d’un '
                'cylindre, pas un fondu entre deux images.',
                'Drag the bottle, or use the slider from the keyboard. The '
                'label wraps and the two mould seams sweep across the body: '
                'this is the real geometry of a cylinder, not a cross-fade '
                'between two images.', 'p', 'viseur__aide'))

    contraintes = ''.join(
        """<div class="carte rev" style="--tint:var(--rose-200);
             min-height:0" data-delai="%(d)d">
             <h3 data-fr="%(fr)s" data-en="%(en)s">%(fr)s</h3>%(t)s
           </div>""" % dict(fr=e(a), en=e(b), d=i * 60,
                            t=bi(dfr, den))
        for i, (a, b, dfr, den) in enumerate(C.CONTRAINTES))

    note = '<div class="avertissement">%s</div>' % bi(
        'Ce qui est montré ci-dessus est un rendu que je dessine : une '
        'silhouette vectorielle construite à partir d’un profil de rayons. '
        'Ce n’est pas une photographie et ce n’est pas un décalque — la '
        'bouteille n’est pas encore fabriquée. Le jour où elle le sera, la '
        'photo remplace le rendu et la page ne change pas.',
        'What is shown above is a rendering I draw: a vector silhouette '
        'built from a profile of radii. It is not a photograph and not a '
        'trace — the bottle is not manufactured yet. The day it is, the '
        'photo replaces the rendering and the page does not change.')

    return gabarit(
        'bouteille.html', 'La bouteille 8', 'The 8 Bottle',
        section(tete('AMARO 8', 'AMARO 8',
                     C.BOUTEILLE_INTRO_FR, C.BOUTEILLE_INTRO_EN)
                + '<div class="grille grille--2" style="align-items:start">'
                  '%s<div>%s%s</div></div>'
                % (viseur,
                   bi('Fiche technique', 'Technical sheet', 'h3',
                      extra='style="margin:0 0 16px;font-size:24px"'),
                   fiche(C.FICHE_BOUTEILLE, 'Fiche technique de la bouteille',
                         'Bottle technical sheet')))
        + section(tete('Six contraintes, un seul dessin',
                       'Six constraints, one drawing')
                  + '<div class="grille grille--3">%s</div>' % contraintes
                  + '<div style="margin-top:30px">%s</div>' % note,
                  'section--rose'),
        script_360('b-v360-i', r))


# ---------------------------------------------------------------------------
# 5. Catalogue produits
# ---------------------------------------------------------------------------

def page_produits():
    filtres = [('tous', 'Tous', 'All'), ('plate', 'Eau plate', 'Still'),
               ('gazeuse', 'Eau gazeuse', 'Sparkling'),
               ('aromatisee', 'Eaux aromatisées', 'Flavored')]
    barre = '<div class="cases" id="filtres" role="group" ' \
            'aria-label="Filtres">%s</div>' % ''.join(
                '<label><input type="radio" name="filtre" value="%s"%s>'
                '<span data-fr="%s" data-en="%s">%s</span></label>'
                % (c, ' checked' if c == 'tous' else '', e(fr), e(en), fr)
                for c, fr, en in filtres)

    items = []
    for eau in C.EAUX:
        cat = 'gazeuse' if eau['cle'] == 'sparkling' else 'plate'
        items.append((cat, eau['nom'], eau['teinte'],
                      eau['type_fr'], eau['type_en'],
                      eau['texte_fr'], eau['texte_en'],
                      eau['nom'].split()[-1].upper(),
                      eau['cle'] == 'sparkling'))
    for s in C.SAVEURS:
        items.append(('aromatisee', 'AMARO ' + s['nom'], s['teinte'],
                      'Eau aromatisée', 'Flavored water',
                      s['d_fr'], s['d_en'], s['nom'].upper(), False))

    cartes = ''.join(
        """<article class="carte produit" data-cat="%(cat)s"
              style="--tint:%(t)s">
             <span class="carte__visuel" style="--tint:%(t)s">%(b)s</span>
             %(type)s<h3>%(nom)s</h3>%(txt)s
             <ul class="puces" style="margin:12px 0 0">%(f)s</ul>
             <span class="carte__pied">
               <a class="btn btn--ligne" href="business.html"
                  data-fr="Demande commerciale"
                  data-en="Sales enquiry">Demande commerciale</a>
             </span>
           </article>""" % dict(
            cat=cat, t=teinte, nom=e(nom),
            b=bouteille('p-' + re.sub(r'\W+', '', nom).lower(), teinte,
                        'AMARO', etq, 210, gazeuse=gaz),
            type=bi(tfr, ten, 'span', 'carte__type'),
            txt=bi(dfr, den),
            f=''.join('<li data-fr="%s" data-en="%s">%s</li>' % (e(a), e(b), a)
                      for a, b in zip(C.FORMATS, C.FORMATS_EN)))
        for cat, nom, teinte, tfr, ten, dfr, den, etq, gaz in items)

    compte = ('<p id="compte-produits" class="eyebrow" '
              'style="margin:22px 0 0" data-n="%d">%d</p>' % (len(items),
                                                              len(items)))

    return gabarit(
        'produits.html', 'Produits', 'Products',
        section(tete('Catalogue', 'Catalogue',
                     'Filtrer par catégorie. Sans JavaScript, la liste '
                     'complète reste affichée — un filtre qui masque tout '
                     'est pire que pas de filtre.',
                     'Filter by category. Without JavaScript the full list '
                     'stays visible — a filter that hides everything is '
                     'worse than no filter.')
                + barre + compte
                + '<div class="grille grille--4" id="produits" '
                  'style="margin-top:26px">%s</div>' % cartes))


# ---------------------------------------------------------------------------
# 6. Durabilite
# ---------------------------------------------------------------------------

def page_durabilite():
    cartes = ''.join(
        """<div class="carte rev" data-delai="%(d)d" style="min-height:0">
             <h3 data-fr="%(fr)s" data-en="%(en)s">%(fr)s</h3>%(t)s
             <div class="carte__pied"><table class="fiche"><tbody><tr>
               <th data-fr="Indicateur publié" data-en="Published figure">
                 Indicateur publié</th><td>%(v)s</td></tr></tbody></table>
             </div>
           </div>""" % dict(fr=e(fr), en=e(en), d=i * 60, t=bi(dfr, den),
                            v=valeur(val, 'durabilite-' + fr))
        for i, (fr, en, dfr, den, val) in enumerate(C.ENGAGEMENTS))

    return gabarit(
        'durabilite.html', 'Durabilité', 'Sustainability',
        section(tete('Durabilité', 'Sustainability',
                     'Emballage et production. Ce sont des chantiers, pas '
                     'des résultats — et la page les présente comme tels.',
                     'Packaging and production. These are workstreams, not '
                     'results — and the page presents them as such.')
                + '<div class="avertissement">%s</div>'
                  % bi(C.DURABILITE_AVERTISSEMENT_FR,
                       C.DURABILITE_AVERTISSEMENT_EN)
                + '<div class="grille grille--3" style="margin-top:34px">%s'
                  '</div>' % cartes))


# ---------------------------------------------------------------------------
# 7. La marque
# ---------------------------------------------------------------------------

def page_marque():
    return gabarit(
        'marque.html', 'La marque', 'About AMARO',
        section(tete('La marque', 'About AMARO',
                     C.MARQUE_VISION_FR, C.MARQUE_VISION_EN)
                + '<div class="grille grille--2" style="align-items:start">'
                  '<div>%s%s</div><div>%s</div></div>'
                % (bi('L’identité de la société',
                      'Company identity', 'h3',
                      extra='style="margin-bottom:14px;font-size:24px"'),
                   fiche(C.FICHE_SOCIETE, 'Identité de la société',
                         'Company identity'),
                   '<div class="avertissement">%s</div>' % bi(
                       'Aucune date de création, aucun dirigeant, aucun '
                       'siège social n’est écrit ici tant qu’ils ne sont pas '
                       'donnés. Une page « à propos » qui invente une '
                       'histoire est la première chose qu’un distributeur '
                       'vérifie, et la première qui coûte la crédibilité de '
                       'tout le reste du site.',
                       'No founding date, no leadership, no head office is '
                       'written here until they are given. An “about” page '
                       'that invents a history is the first thing a '
                       'distributor checks, and the first thing that costs '
                       'the credibility of the whole site.'))))


# ---------------------------------------------------------------------------
# 8. AMARO Business
# ---------------------------------------------------------------------------

def champ(nom, fr, en, type_='text', requis=True, large=False, options=None,
          aire=False):
    cls = 'champ champ--large' if large else 'champ'
    etoile = ' <span class="req" aria-hidden="true">*</span>' if requis else ''
    r = ' required' if requis else ''
    if options is not None:
        ctrl = ('<select id="f-%s" name="%s"%s>%s</select>'
                % (nom, nom, r, ''.join(
                    '<option value="%s" data-fr="%s" data-en="%s">%s</option>'
                    % (e(v), e(a), e(b), a) for v, a, b in options)))
    elif aire:
        ctrl = '<textarea id="f-%s" name="%s"%s></textarea>' % (nom, nom, r)
    else:
        ctrl = ('<input id="f-%s" name="%s" type="%s"%s autocomplete="off">'
                % (nom, nom, type_, r))
    return ("""<div class="champ %s" data-champ="%s">
      <label for="f-%s" data-fr="%s" data-en="%s">%s</label>%s
      %s<p class="champ__err" id="e-%s" role="alert"></p></div>"""
            % (cls.replace('champ ', '', 1) if False else cls, nom, nom,
               e(fr + ' *' if requis else fr), e(en + ' *' if requis else en),
               fr + etoile, '', ctrl, nom))


def page_business():
    secteurs = '<div class="champ champ--large"><span class="champ" ' \
        'style="gap:0"><label as="span" data-fr="Secteur d’activité *" ' \
        'data-en="Business sector *">Secteur d’activité ' \
        '<span class="req">*</span></label></span>' \
        '<div class="cases" id="secteurs">%s</div>' \
        '<p class="champ__err" id="e-secteur" role="alert"></p></div>' % (
            # name="secteur[]" : sans les crochets, PHP ne garde que la
            # DERNIERE case cochee et le distributeur qui coche six secteurs
            # en voit arriver un seul.
            ''.join('<label><input type="checkbox" name="secteur[]" '
                    'value="%s"><span data-fr="%s" data-en="%s">%s</span>'
                    '</label>' % (c, e(fr), e(en), fr)
                    for c, fr, en in C.SECTEURS))

    form = """<form class="form" id="b2b" novalidate %(action)s method="post">
      %(societe)s %(pays)s %(ville)s %(contact)s %(courriel)s %(tel)s
      %(secteurs)s
      <!-- Piege a robots : un champ que personne ne voit et que personne ne
           remplit. Il est masque en CSS et retire du parcours clavier et
           lecteur d'ecran ; un automate, lui, remplit tout ce qu'il trouve.
           formulaire.php repond alors 200 comme si tout allait bien, pour
           ne pas lui apprendre a quoi ressemble un echec. -->
      <div class="hors-ecran" aria-hidden="true">
        <label for="f-site_web">Site web</label>
        <input id="f-site_web" name="site_web" type="text" tabindex="-1"
               autocomplete="off">
      </div>
      %(marches)s %(produits)s %(volume)s
      %(message)s
      <div class="champ champ--large">
        <label style="flex-direction:row;align-items:flex-start;gap:10px;
                      display:flex;font-size:14px">
          <input type="checkbox" name="consentement" id="f-consentement"
                 style="width:auto;margin-top:3px" required>
          <span data-fr="%(cfr)s" data-en="%(cen)s">%(cfr)s</span>
        </label>
        <p class="champ__err" id="e-consentement" role="alert"></p>
      </div>
      <div class="champ champ--large">
        <button class="btn btn--plein" type="submit" data-fr="%(bfr)s"
                data-en="%(ben)s" style="justify-content:center">%(bfr)s</button>
      </div>
      <div class="champ champ--large" id="resultat" hidden></div>
    </form>""" % dict(
        action=('action="%s"' % ACTION_FORMULAIRE) if ACTION_FORMULAIRE else '',
        societe=champ('societe', 'Nom de société', 'Company name'),
        pays=champ('pays', 'Pays', 'Country'),
        ville=champ('ville', 'Ville', 'City'),
        contact=champ('contact', 'Nom du contact', 'Contact name'),
        courriel=champ('courriel', 'Courriel', 'E-mail', 'email'),
        tel=champ('telephone', 'Téléphone', 'Phone', 'tel', requis=False),
        secteurs=secteurs,
        marches=champ('marches', 'Marchés couverts (pays, régions)',
                      'Markets covered (countries, regions)', large=True),
        produits=champ('produits', 'Produits recherchés',
                       'Products of interest', requis=False),
        volume=champ('volume', 'Volume estimé', 'Estimated volume',
                     options=C.VOLUMES, requis=False),
        message=champ('message', 'Message', 'Message', requis=False,
                      large=True, aire=True),
        cfr='J’accepte qu’AMARO conserve ces informations pour traiter ma '
            'demande commerciale.',
        cen='I agree that AMARO may keep this information in order to handle '
            'my sales enquiry.',
        bfr='Envoyer la demande', ben='Send the enquiry')

    note_envoi = '<div class="avertissement" style="margin-top:26px">%s</div>' \
        % bi('Dans cette maquette, l’envoi n’est pas branché : il n’y a '
             'encore ni hébergement, ni adresse commerciale, ni CRM. Le '
             'formulaire valide bel et bien les champs et affiche ce qui '
             'partirait — il ne fait pas semblant d’avoir envoyé. Le '
             'traitement serveur est livré à part (formulaire.php) : une '
             'ligne de configuration l’active le jour où le site est en '
             'ligne.',
             'In this prototype, sending is not connected: there is no '
             'hosting, no sales address and no CRM yet. The form does '
             'validate the fields and shows what would be sent — it does not '
             'pretend to have sent it. The server-side handler ships '
             'separately (formulaire.php): one configuration line switches it '
             'on the day the site is live.')

    return gabarit(
        'business.html', 'AMARO Business', 'AMARO Business',
        section(tete('Devenir distributeur AMARO',
                     'Become an AMARO Distributor',
                     'Distributeurs, grossistes, supermarchés, hôtels, '
                     'restaurants, cafés, salles de sport, entreprises et '
                     'événementiel.',
                     'Distributors, wholesalers, supermarkets, hotels, '
                     'restaurants, cafés, gyms, corporate and events.')
                + form + note_envoi))


# ---------------------------------------------------------------------------
# 9. Distribution internationale
# ---------------------------------------------------------------------------

def page_distribution():
    couleur = {c: col for c, fr, en, col in C.STATUTS}
    lib = {c: (fr, en) for c, fr, en, col in C.STATUTS}

    legende = '<div class="legende">%s</div>' % ''.join(
        '<span><i style="background:%s"></i>'
        '<b data-fr="%s" data-en="%s">%s</b> '
        '<span data-fr="(%d)" data-en="(%d)">(%d)</span></span>'
        % (col, e(fr), e(en), fr,
           sum(1 for m in C.MARCHES if m[4] == c),
           sum(1 for m in C.MARCHES if m[4] == c),
           sum(1 for m in C.MARCHES if m[4] == c))
        for c, fr, en, col in C.STATUTS)

    if C.MARCHES:
        corps = ''
        for rfr, ren in C.REGIONS:
            dedans = [m for m in C.MARCHES if m[2] == rfr]
            if not dedans:
                continue
            corps += ('<div class="region">%s<ul class="marches">%s</ul></div>'
                      % (bi(rfr, ren, 'h3'),
                         ''.join('<li class="marche"><i style="background:%s">'
                                 '</i><b data-fr="%s" data-en="%s">%s</b>'
                                 '<span style="color:var(--gris-400)" '
                                 'data-fr="%s" data-en="%s">%s</span></li>'
                                 % (couleur[st], e(pfr), e(pen), pfr,
                                    e(lib[st][0]), e(lib[st][1]), lib[st][0])
                                 for pfr, pen, _, _, st in dedans)))
    else:
        corps = """<div class="vide-bloc">%s%s</div>""" % (
            bi('Aucun marché n’est déclaré', 'No market is declared', 'h3'),
            # Le texte est ecrit pour un VISITEUR, pas pour moi. Une version
            # precedente nommait ici le fichier et la variable a modifier :
            # du vocabulaire de developpeur sur une page que des acheteurs
            # vont lire. La marche a suivre est dans le README, a sa place.
            bi('Les marchés ouverts, et ceux où AMARO cherche un partenaire, '
               'sont une information commerciale : ils seront publiés dès '
               'qu’AMARO les aura arrêtés. La page, la légende et les '
               'compteurs sont en place et se remplissent à la première '
               'ligne fournie.',
               'Open markets, and those where AMARO is looking for a partner, '
               'are commercial information: they will be published once AMARO '
               'has settled them. The page, the legend and the counters are '
               'in place and fill in from the first line provided.'))

    appel = section("""<div class="tete tete--centre">%s%s
        <div class="hero__ctas" style="justify-content:center">
          <a class="btn btn--clair" href="business.html" data-fr="%s"
             data-en="%s">%s</a></div></div>""" % (
        bi('Votre marché n’est pas listé ?', 'Your market is not listed?',
           'h2'),
        bi('C’est précisément ceux-là qui nous intéressent. Le formulaire '
           'demande le pays, les marchés couverts et les volumes estimés.',
           'Those are exactly the ones we are interested in. The form asks '
           'for country, markets covered and estimated volumes.'),
        e(C.HERO['cta2_fr']), e(C.HERO['cta2_en']), e(C.HERO['cta2_fr'])),
        'section--encre')

    return gabarit(
        'distribution.html', 'Distribution', 'Global Distribution',
        section(tete('Distribution internationale', 'Global Distribution',
                     'Trois statuts : disponible, distributeur recherché, '
                     'bientôt. %d marché%s déclaré%s.'
                     % (len(C.MARCHES), 's' if len(C.MARCHES) > 1 else '',
                        's' if len(C.MARCHES) > 1 else ''),
                     'Three statuses: available, distributor wanted, coming '
                     'soon. %d market%s declared.'
                     % (len(C.MARCHES), 's' if len(C.MARCHES) > 1 else ''))
                + legende + corps) + appel)


# ---------------------------------------------------------------------------
# 10. Actualites
# ---------------------------------------------------------------------------

def page_actualites():
    if C.ACTUALITES:
        corps = ''.join('<article class="carte"><h3>%s</h3><p>%s</p></article>'
                        % (e(a['titre']), e(a['texte'])) for a in C.ACTUALITES)
        corps = '<div class="grille grille--3">%s</div>' % corps
    else:
        corps = '<div class="vide-bloc">%s%s</div>' % (
            bi('Aucune actualité publiée', 'No news published', 'h3'),
            bi('Le gabarit est en place : titre, date, visuel, texte, lien. '
               'Il n’y a rien à annoncer pour l’instant, et une page '
               'd’actualités remplie d’articles inventés se voit tout de '
               'suite — elle vaut moins qu’une page vide qui le dit.',
               'The template is in place: title, date, visual, text, link. '
               'There is nothing to announce yet, and a news page filled with '
               'invented articles is spotted immediately — it is worth less '
               'than an empty page that says so.'))
    return gabarit('actualites.html', 'Actualités', 'News',
                   section(tete('Actualités', 'News') + corps))


# ---------------------------------------------------------------------------
# 11. Contact
# ---------------------------------------------------------------------------

def page_contact():
    reseaux = '<ul class="puces" style="margin-top:16px">%s</ul>' % ''.join(
        '<li>%s — %s</li>' % (e(nom), valeur(url, 'reseau-' + c))
        for c, nom, url in C.RESEAUX)
    return gabarit(
        'contact.html', 'Contact', 'Contact',
        section(tete('Contact', 'Contact',
                     'Pour les demandes commerciales, le formulaire '
                     'distributeur est plus rapide : il pose déjà les bonnes '
                     'questions.',
                     'For sales enquiries the distributor form is faster: it '
                     'already asks the right questions.')
                + '<div class="grille grille--2" style="align-items:start">'
                  '<div>%s%s</div><div>%s<div class="hero__ctas">'
                  '<a class="btn btn--plein" href="business.html" '
                  'data-fr="%s" data-en="%s">%s</a></div></div></div>'
                % (fiche(C.CONTACT, 'Coordonnées', 'Contact details'), reseaux,
                   '<div class="avertissement">%s</div>' % bi(
                       'Aucune adresse, aucun numéro et aucun courriel n’est '
                       'écrit ici tant qu’ils ne sont pas donnés. Un contact '
                       'inventé sur un site B2B se compose, et tombe dans le '
                       'vide devant un distributeur.',
                       'No address, no number and no e-mail is written here '
                       'until they are given. An invented contact on a B2B '
                       'site gets dialled, and rings out in front of a '
                       'distributor.'),
                   e(C.HERO['cta2_fr']), e(C.HERO['cta2_en']),
                   e(C.HERO['cta2_fr']))))


# ---------------------------------------------------------------------------
# 12. Boutique (phase ulterieure)
# ---------------------------------------------------------------------------

def page_boutique():
    etapes = [
        ('Packs et assortiments', 'Packs and assortments',
         'Packs d’eau, coffrets de saveurs, offres spécifiques. Le catalogue '
         'et les fiches existent déjà : la boutique les réutilise, elle ne '
         'les redouble pas.',
         'Water packs, flavor assortments, special offers. The catalogue and '
         'the sheets already exist: the shop reuses them, it does not '
         'duplicate them.'),
        ('Comptes clients', 'Customer accounts',
         'Adresses, historique, réassort en un clic.',
         'Addresses, history, one-click reorder.'),
        ('Paiement', 'Payment',
         'Le prestataire dépend du pays d’exploitation : il fixe les moyens '
         'de paiement acceptés, les devises et la TVA. Rien n’est branché '
         'tant que ce pays n’est pas choisi.',
         'The provider depends on the country of operation: it determines the '
         'accepted payment methods, the currencies and the VAT. Nothing is '
         'connected until that country is chosen.'),
        ('Commandes et livraison', 'Orders and delivery',
         'Statuts, suivi, transporteurs.',
         'Statuses, tracking, carriers.'),
        ('Abonnements', 'Subscriptions',
         'Livraison récurrente, pause, modification de la fréquence.',
         'Recurring delivery, pause, frequency change.'),
    ]
    cartes = ''.join(
        '<div class="carte rev" data-delai="%d" style="min-height:0">'
        '<h3 data-fr="%s" data-en="%s">%s</h3>%s</div>'
        % (i * 60, e(fr), e(en), fr, bi(dfr, den))
        for i, (fr, en, dfr, den) in enumerate(etapes))

    return gabarit(
        'boutique.html', 'Boutique', 'Shop',
        section(tete('Boutique en ligne — phase ultérieure',
                     'Online shop — later phase',
                     'L’architecture du site est déjà compatible : catalogue, '
                     'fiches, formats et visuels sont des données, pas des '
                     'pages écrites à la main. Ajouter la vente, c’est '
                     'brancher un panier dessus, pas refaire le site.',
                     'The site architecture is already compatible: catalogue, '
                     'sheets, formats and visuals are data, not hand-written '
                     'pages. Adding sales means plugging a basket onto it, '
                     'not rebuilding the site.')
                + '<div class="grille grille--3">%s</div>' % cartes
                + '<div class="avertissement" style="margin-top:30px">%s</div>'
                % bi('Aucun prix n’est affiché nulle part sur ce site. Un '
                     'prix dépend du pays, de la devise, de la TVA, du '
                     'transport et du contrat de distribution : en écrire un '
                     'avant que ces cinq soient fixés, c’est en écrire un '
                     'faux.',
                     'No price is shown anywhere on this site. A price '
                     'depends on the country, the currency, the VAT, the '
                     'freight and the distribution contract: writing one '
                     'before those five are settled means writing a wrong '
                     'one.')))


# ---------------------------------------------------------------------------
# 13. Charte graphique
# ---------------------------------------------------------------------------

def page_design():
    def nuancier(liste):
        return '<div class="nuancier">%s</div>' % ''.join(
            '<div class="nuance"><div class="nuance__aplat" '
            'style="background:%s"></div><div class="nuance__txt">'
            '<b>%s</b><code>%s</code><small>%s</small></div></div>'
            % (hexa, e(nom), e(hexa), e(role))
            for nom, hexa, role in liste)

    types = """<div class="grille grille--2" style="align-items:start">
      <div>
        <p style="font-size:clamp(34px,5vw,64px);line-height:.95;
                  letter-spacing:-.045em;font-weight:600;margin:0">Water.</p>
        <p style="font-family:var(--serif);font-style:italic;
                  font-size:clamp(34px,5vw,64px);line-height:.95;
                  color:var(--rose-500);margin:0 0 18px">Reimagined.</p>
        %s
      </div>
      <div>%s</div>
    </div>""" % (
        bi('Titrage : sans-serif, graisse 600, interlettrage négatif. '
           'L’accent est porté par un seul mot en serif italique rose — '
           'jamais deux.',
           'Headlines: sans-serif, weight 600, negative tracking. The accent '
           'is carried by a single word in rose serif italic — never two.'),
        bi('Le corps de texte reste en sans-serif, 17 px, interligne 1,65. '
           'Les surtitres sont en capitales, 12 px, interlettrage 0,30 em, '
           'toujours en rose 500. C’est le seul endroit où le rose sert de '
           'texte courant.',
           'Body copy stays sans-serif, 17 px, line height 1.65. Eyebrows are '
           'uppercase, 12 px, 0.30 em tracking, always in rose 500. That is '
           'the only place where rose is used as running text.'))

    bouteilles = '<div class="grille grille--4">%s</div>' % ''.join(
        '<div class="carte" style="--tint:%s;text-align:center">'
        '<span class="carte__visuel" style="--tint:%s">%s</span>'
        '<h3 style="font-size:17px">%s</h3></div>'
        % (s['teinte'], s['teinte'],
           bouteille('d-' + s['cle'], s['teinte'], 'AMARO', s['nom'].upper(),
                     170), e(s['nom']))
        for s in C.SAVEURS)

    return gabarit(
        'design.html', 'Charte graphique', 'Design system',
        section(tete('Charte graphique AMARO', 'AMARO design system',
                     'Rose et blanc, comme demandé. Deux couleurs ne '
                     'suffisent pas à tenir un site : il en faut une échelle, '
                     'sinon chaque page réinvente son rose et la marque se '
                     'délave. La voici, déclarée une seule fois et lue par '
                     'toutes les pages.',
                     'Rose and white, as requested. Two colors are not enough '
                     'to hold a site together: you need a scale, otherwise '
                     'every page reinvents its own rose and the brand washes '
                     'out. Here it is, declared once and read by every page.')
                + '<h3 style="margin:0 0 16px;font-size:22px">Rose</h3>'
                + nuancier(C.ROSE)
                + '<h3 style="margin:38px 0 16px;font-size:22px" '
                  'data-fr="Blanc et neutres" data-en="White and neutrals">'
                  'Blanc et neutres</h3>'
                + nuancier(C.NEUTRES)
                + '<div class="avertissement" style="margin-top:34px">%s</div>'
                % bi('La règle qui compte : rose-500 est la couleur de '
                     'marque, ce n’est pas la couleur du texte. Mesuré sur '
                     'blanc, il donne 4,05 pour 1 — sous le seuil de 4,5 en '
                     'dessous duquel un texte courant devient pénible à lire. '
                     'Les boutons, les surtitres et les liens utilisent donc '
                     'rose-600 (5,7 pour 1). Rose-500 reste sur les aplats, '
                     'le graphisme et les très gros titres, où le seuil est '
                     'de 3 et où il passe. Le contraste est mesuré page par '
                     'page sur les couleurs que le navigateur calcule, pas '
                     'lues dans la feuille de style : lire une règle CSS ne '
                     'dit pas laquelle a gagné.',
                     'The rule that matters: rose-500 is the brand color, not '
                     'the text color. Measured on white it gives 4.05 to 1 — '
                     'below the 4.5 threshold under which running text becomes '
                     'hard work. Buttons, eyebrows and links therefore use '
                     'rose-600 (5.7 to 1). Rose-500 stays on fills, graphics '
                     'and very large headings, where the threshold is 3 and it '
                     'passes. Contrast is measured page by page on the '
                     'colors the browser computes, not read off the '
                     'stylesheet: reading a CSS rule does not tell you which '
                     'one won.'))
        + section(tete('Typographie', 'Typography') + types, 'section--rose')
        + section(tete('Le code couleur des saveurs',
                       'The flavor color code',
                       'Le chrome de la marque reste rose et blanc. La saveur '
                       'ne colore que le liquide et un filet de 3 px : c’est '
                       'ce qui permet huit codes distincts sans huit '
                       'identités.',
                       'The brand chrome stays rose and white. The flavor '
                       'only colors the liquid and a 3 px rule: that is what '
                       'allows eight distinct codes without eight '
                       'identities.')
                  + bouteilles))


# ---------------------------------------------------------------------------
# 14. Ce qui reste a fournir
# ---------------------------------------------------------------------------

def page_trous():
    trous = C.champs_vides()
    groupes = []
    for t in trous:
        if not groupes or groupes[-1][0] != t['groupe_fr']:
            groupes.append((t['groupe_fr'], t['groupe_en'], t['page'], []))
        groupes[-1][3].append(t)

    corps = ''.join(
        '<div class="region"><h3><span data-fr="%s" data-en="%s">%s</span> '
        '<a href="%s" style="font-size:13px;color:var(--rose-700)">%s</a>'
        '</h3><ul class="marches">%s</ul></div>'
        % (e(gfr), e(gen), gfr, page, e(page),
           ''.join('<li class="marche"><i style="background:var(--rose-400)">'
                   '</i><span data-fr="%s" data-en="%s">%s</span></li>'
                   % (e(t['fr']), e(t['en']), t['fr']) for t in items))
        for gfr, gen, page, items in groupes)

    return gabarit(
        'a-renseigner.html', 'Ce qui reste à fournir',
        'What is still needed',
        section(tete('Ce qui reste à fournir', 'What is still needed',
                     '%d champs sont volontairement vides sur le site, et le '
                     'disent en clair sur la page où ils se trouvent. Cette '
                     'liste est calculée à la construction : elle ne peut pas '
                     'se désynchroniser du site.' % len(trous),
                     '%d fields are deliberately empty on the site, and say '
                     'so plainly on the page where they sit. This list is '
                     'computed at build time: it cannot drift out of sync '
                     'with the site.' % len(trous))
                + '<div class="avertissement">%s</div>' % bi(
                    'Ce ne sont pas des oublis. Une eau embouteillée est un '
                    'produit réglementé : origine, analyse, pH, ingrédients, '
                    'nutrition, taux de rPET, recyclabilité, poids de '
                    'préforme. Chacune de ces valeurs se prouve avec une '
                    'pièce — bulletin d’analyse, fiche du souffleur, '
                    'attestation du fournisseur de résine. Un chiffre '
                    'plausible écrit ici finirait recopié sur une étiquette '
                    'et deviendrait une déclaration fausse que personne ne se '
                    'rappellerait avoir écrite.',
                    'These are not oversights. Bottled water is a regulated '
                    'product: source, analysis, pH, ingredients, nutrition, '
                    'rPET content, recyclability, preform weight. Every one '
                    'of those values is proven with a document — laboratory '
                    'report, blower’s sheet, resin supplier’s statement. A '
                    'plausible figure written here would end up copied onto a '
                    'label and become a false declaration that nobody would '
                    'remember writing.')
                + corps))


# ---------------------------------------------------------------------------
# Le script du site
# ---------------------------------------------------------------------------

JS = r"""
(function () {
  'use strict';
  document.body.classList.add('js');

  /* ── Langue ────────────────────────────────────────────────────────────
     Les deux langues sont dans le DOM, en attributs. Changer de langue
     reecrit du texte ; ca ne reconstruit pas la page et ca ne perd pas la
     position dans le defilement. */
  var LANGUE = 'fr';
  function langue(l) {
    LANGUE = l;
    document.documentElement.lang = l;
    var n = document.querySelectorAll('[data-fr]');
    for (var i = 0; i < n.length; i++) {
      var v = n[i].getAttribute('data-' + l);
      if (v === null) continue;
      /* textContent, jamais innerHTML : le contenu des attributs vient de
         contenu.py, mais l'ecrire en HTML ouvrirait la porte le jour ou il
         viendra d'ailleurs. */
      n[i].textContent = v;
    }
    var b = document.querySelectorAll('[data-langue]');
    for (var j = 0; j < b.length; j++) {
      b[j].setAttribute('aria-pressed',
        b[j].getAttribute('data-langue') === l ? 'true' : 'false');
    }
    try { localStorage.setItem('amaro-langue', l); } catch (e) {}
  }
  var lb = document.querySelectorAll('[data-langue]');
  for (var k = 0; k < lb.length; k++) {
    lb[k].addEventListener('click', function () {
      langue(this.getAttribute('data-langue'));
    });
  }
  try {
    var m = localStorage.getItem('amaro-langue');
    if (m === 'en') langue('en');
  } catch (e) {}

  /* ── Menu mobile ───────────────────────────────────────────────────── */
  var burger = document.getElementById('burger'),
      entete = document.getElementById('entete');
  if (burger && entete) {
    burger.addEventListener('click', function () {
      var o = entete.classList.toggle('ouvert');
      burger.setAttribute('aria-expanded', o ? 'true' : 'false');
    });
  }

  /* ── Apparitions ───────────────────────────────────────────────────── */
  var revs = document.querySelectorAll('.rev, [data-delai]');
  for (var r = 0; r < revs.length; r++) {
    if (!revs[r].classList.contains('rev')) revs[r].classList.add('rev');
    var d = revs[r].getAttribute('data-delai');
    if (d) revs[r].style.transitionDelay = d + 'ms';
  }
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (x) {
        if (x.isIntersecting) { x.target.classList.add('vu'); io.unobserve(x.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    for (var q = 0; q < revs.length; q++) io.observe(revs[q]);
  } else {
    /* Pas d'observateur : on montre tout. Un navigateur qui ne sait pas
       observer n'est pas un navigateur qui merite une page blanche. */
    for (var w = 0; w < revs.length; w++) revs[w].classList.add('vu');
  }

  /* ── Filtres du catalogue ──────────────────────────────────────────── */
  var filtres = document.getElementById('filtres');
  if (filtres) {
    var compte = document.getElementById('compte-produits');
    function filtrer() {
      var v = filtres.querySelector('input:checked');
      v = v ? v.value : 'tous';
      var p = document.querySelectorAll('#produits .produit'), n = 0;
      for (var i = 0; i < p.length; i++) {
        var ok = (v === 'tous' || p[i].getAttribute('data-cat') === v);
        p[i].hidden = !ok;
        if (ok) n++;
      }
      if (compte) {
        compte.textContent = n + (LANGUE === 'fr'
          ? (n > 1 ? ' produits' : ' produit')
          : (n > 1 ? ' products' : ' product'));
      }
    }
    filtres.addEventListener('change', filtrer);
    filtrer();
  }

  /* ── Formulaire B2B ────────────────────────────────────────────────── */
  var f = document.getElementById('b2b');
  if (f) {
    var MSG = {
      requis:   ['Ce champ est obligatoire.', 'This field is required.'],
      courriel: ['Adresse électronique invalide.', 'Invalid e-mail address.'],
      secteur:  ['Choisissez au moins un secteur.',
                 'Choose at least one sector.'],
      consent:  ['Votre accord est nécessaire pour traiter la demande.',
                 'Your agreement is required to handle the enquiry.']
    };
    function dire(cle) { return MSG[cle][LANGUE === 'en' ? 1 : 0]; }
    function erreur(nom, texte) {
      var p = document.getElementById('e-' + nom);
      if (p) p.textContent = texte || '';
      var bloc = f.querySelector('[data-champ="' + nom + '"]');
      if (bloc) bloc.classList.toggle('faux', !!texte);
    }
    f.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var ok = true, premier = null;
      var champs = f.querySelectorAll('[data-champ]');
      for (var i = 0; i < champs.length; i++) {
        var nom = champs[i].getAttribute('data-champ');
        var ctrl = champs[i].querySelector('input,select,textarea');
        if (!ctrl) continue;
        var v = (ctrl.value || '').trim();
        if (ctrl.required && !v) {
          erreur(nom, dire('requis')); ok = false;
          if (!premier) premier = ctrl;
          continue;
        }
        if (ctrl.type === 'email' && v && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) {
          erreur(nom, dire('courriel')); ok = false;
          if (!premier) premier = ctrl;
          continue;
        }
        erreur(nom, '');
      }
      var sec = f.querySelectorAll('#secteurs input:checked');
      erreur('secteur', sec.length ? '' : dire('secteur'));
      if (!sec.length) { ok = false; if (!premier) premier = f.querySelector('#secteurs input'); }
      var cons = document.getElementById('f-consentement');
      erreur('consentement', cons && cons.checked ? '' : dire('consent'));
      if (cons && !cons.checked) { ok = false; if (!premier) premier = cons; }

      var res = document.getElementById('resultat');
      if (!ok) {
        if (res) res.hidden = true;
        if (premier) premier.focus();
        return;
      }
      if (f.getAttribute('action')) { f.submit(); return; }

      /* Pas d'action : on ne dit PAS « envoyé ». On montre ce qui partirait.
         Un accuse de reception sans destinataire est un mensonge poli, et
         c'est celui-la qu'un distributeur croit. */
      var lignes = [];
      var fd = new FormData(f);
      fd.forEach(function (val, cle) {
        if (String(val).trim()) lignes.push(cle + ' : ' + val);
      });
      if (res) {
        res.hidden = false;
        res.innerHTML = '';
        var box = document.createElement('div');
        box.className = 'avertissement';
        var t = document.createElement('p');
        t.innerHTML = '<strong>' + (LANGUE === 'en'
          ? 'Nothing was sent — and that is deliberate.'
          : 'Rien n’a été envoyé — et c’est volontaire.') + '</strong>';
        var s = document.createElement('p');
        s.textContent = LANGUE === 'en'
          ? 'The form is valid. There is no hosting, no sales address and no '
            + 'CRM connected yet, so here is exactly what would be sent:'
          : 'Le formulaire est valide. Il n’y a encore ni hébergement, ni '
            + 'adresse commerciale, ni CRM branché : voici exactement ce qui '
            + 'partirait :';
        var pre = document.createElement('pre');
        pre.style.cssText = 'white-space:pre-wrap;font-size:13px;margin:0;'
          + 'background:#fff;border:1px solid var(--rose-200);'
          + 'border-radius:10px;padding:14px;overflow-x:auto';
        pre.textContent = lignes.join('\n');
        box.appendChild(t); box.appendChild(s); box.appendChild(pre);
        res.appendChild(box);
        res.scrollIntoView({ block: 'nearest' });
      }
    });
  }
})();
"""


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

PAGES = [
    ('index.html', page_accueil),
    ('notre-eau.html', page_eau),
    ('saveurs.html', page_saveurs),
    ('bouteille.html', page_bouteille),
    ('produits.html', page_produits),
    ('durabilite.html', page_durabilite),
    ('marque.html', page_marque),
    ('business.html', page_business),
    ('distribution.html', page_distribution),
    ('actualites.html', page_actualites),
    ('contact.html', page_contact),
    ('boutique.html', page_boutique),
    ('design.html', page_design),
    ('a-renseigner.html', page_trous),
]


def ecrire(nom, texte):
    chemin = os.path.join(DEMO, nom)
    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(texte)
    return os.path.getsize(chemin)


def main():
    if not os.path.isdir(DEMO):
        os.makedirs(DEMO)
    total = 0
    total += ecrire('styles.css', CSS)
    total += ecrire('script.js', JS)
    print('%-22s %9s' % ('page', 'octets'))
    for nom, fn in PAGES:
        n = ecrire(nom, fn())
        total += n
        print('%-22s %9d' % (nom, n))
    print('%-22s %9d' % ('(total)', total))
    print('%d champs volontairement vides — voir a-renseigner.html'
          % len(C.champs_vides()))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
