# -*- coding: utf-8 -*-
"""La bouteille AMARO 8, dessinee en SVG.

CE QUE C'EST, ET CE QUE CE N'EST PAS
────────────────────────────────────
C'est un RENDU que je dessine : une silhouette vectorielle construite a
partir d'un profil de rayons, pas une photographie et pas un decalque. La
bouteille n'est pas encore fabriquee ; publier une image qui ressemble a une
photo de produit ferait passer un projet pour un objet en stock. Le site le
dit sur la page bouteille.

LE PROFIL
─────────
Le corps est defini par une liste de couples (y, demi-largeur). Tout le reste
en decoule : le contour, la matiere, le liquide, la couture de moule et
l'etiquette. Changer la forme = changer PROFIL, rien d'autre.

LE 360°
───────
Une bouteille de section circulaire a la MEME silhouette sous tous les
angles : la faire tourner ne change pas son contour, ca change ce qui est
ecrit dessus. Le visualiseur applique donc la vraie geometrie du cylindre :

    un point a l'azimut t, sur un rayon r, se projette en x = r · sin(t + a)
    et n'est visible que si cos(t + a) > 0.

L'etiquette de face (azimut 0) glisse donc en r·sin(a) et s'ecrase en cos(a) ;
le panneau arriere (azimut pi) apparait quand la face disparait ; les deux
coutures de moule (azimut ±pi/2) balaient le corps. C'est un vrai tour, pas
un fondu entre deux images.
"""

import math

# Le repere du dessin. Tout est en unites de viewBox ; l'echelle se fait a
# l'affichage avec width/height.
LARGEUR = 240
HAUTEUR = 620
CX = 120.0

# Profil du corps : (y, demi-largeur). Du haut du col jusqu'au pied.
#
# CE PROFIL EST LA MARQUE. Il a ete refait apres avoir REGARDE le premier
# rendu : la taille n'y etait pincee qu'a 47 % du plus large, et entre y=196
# et y=228 la demi-largeur ne bougeait pas — un segment droit de 30 px. Le
# resultat se lisait comme une bouteille d'eau ordinaire avec un creux, pas
# comme un 8. Aucun controle automatique n'aurait pu le dire ; il fallait
# ouvrir la capture.
#
# Ce qui a change, et ce qu'il faut preserver si le profil est retouche :
#
#   - la TAILLE (y=312) est a 38 contre 92 au plus large, soit 41 %. C'est
#     le pincement qui fait le 8, et c'est aussi la zone la plus sollicitee
#     de la bouteille — la fiche technique lui reserve une ligne d'epaisseur ;
#   - les DEUX LOBES sont convexes d'un bout a l'autre. Pas un seul palier :
#     un palier se lit comme un cylindre et casse la lecture ;
#   - le pied REVIENT vers l'interieur (92 au ventre bas, 61 au talon). Sans
#     ce retrait, le lobe du bas n'a pas de bas et le 8 redevient une poire.
#   - l'EPAULE monte vite (16 a y=82, deja 62 a y=127). Etalee sur 80 px,
#     elle fondait le lobe du haut dans le col et la silhouette se lisait
#     comme une gourde ; un lobe est un volume, il doit commencer quelque
#     part.
PROFIL = [
    (64, 16), (82, 16.5), (94, 21), (104, 33), (115, 48), (127, 62),
    (141, 73), (158, 81), (178, 85.5), (198, 86.5), (218, 84), (236, 78),
    (254, 69), (272, 58), (288, 47), (302, 40), (312, 38), (326, 40),
    (342, 48), (360, 60), (380, 72), (402, 83), (424, 90), (448, 92),
    (472, 91.5), (496, 88), (518, 82), (538, 74), (554, 66), (564, 61),
]

Y_BASE = 580.0          # le pied
Y_ETIQUETTE = (398.0, 492.0)    # la bande d'etiquette, sur le lobe bas
Y_TAILLE = 312.0

CAP_HAUT = 10.0
CAP_BAS = 50.0
CAP_DEMI = 21.0
BAGUE_BAS = 64.0
BAGUE_DEMI = 25.0


def rayon(y):
    """Demi-largeur du corps a la hauteur y, interpolee lineairement.

    Sert a poser l'etiquette et a calculer le glissement du 360 : sans elle,
    l'etiquette tournerait sur un rayon constant et se decollerait du corps
    au niveau des epaules.
    """
    if y <= PROFIL[0][0]:
        return float(PROFIL[0][1])
    if y >= PROFIL[-1][0]:
        return float(PROFIL[-1][1])
    for i in range(len(PROFIL) - 1):
        y0, h0 = PROFIL[i]
        y1, h1 = PROFIL[i + 1]
        if y0 <= y <= y1:
            t = (y - y0) / float(y1 - y0)
            return h0 + (h1 - h0) * t
    return float(PROFIL[-1][1])


def _catmull(points):
    """Convertit une polyligne en courbes de Bezier lisses.

    Sans lissage, le profil se lit comme une suite de facettes : une
    bouteille soufflee n'a pas d'aretes, et l'oeil le voit tout de suite.
    """
    pts = [points[0]] + list(points) + [points[-1]]
    d = []
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6.0, p1[1] + (p2[1] - p0[1]) / 6.0)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6.0, p2[1] - (p3[1] - p1[1]) / 6.0)
        d.append('C%.2f %.2f %.2f %.2f %.2f %.2f'
                 % (c1[0], c1[1], c2[0], c2[1], p2[0], p2[1]))
    return ' '.join(d)


def _cote_droit():
    return [(CX + h, y) for y, h in PROFIL]


def chemin_profil_droit():
    """Le flanc droit seul — c'est lui qu'on ecrase pour tracer une couture."""
    pts = _cote_droit()
    return 'M%.2f %.2f %s' % (pts[0][0], pts[0][1], _catmull(pts))


def chemin_corps():
    """Le contour ferme du corps, col compris, avec un pied a fond petaloide."""
    droite = _cote_droit()
    gauche = [(CX - (x - CX), y) for x, y in reversed(droite)]
    d = ['M%.2f %.2f' % droite[0]]
    d.append(_catmull(droite))
    # Le pied : on descend au rayon du talon, on traverse, et le fond remonte
    # legerement au centre — un fond plat de PET ne tient pas la pression.
    xd, yd = droite[-1]
    xg = CX - (xd - CX)
    d.append('C%.2f %.2f %.2f %.2f %.2f %.2f'
             % (xd, Y_BASE - 4, xd - 8, Y_BASE, xd - 20, Y_BASE))
    d.append('C%.2f %.2f %.2f %.2f %.2f %.2f'
             % (CX + 24, Y_BASE, CX + 18, Y_BASE - 13, CX, Y_BASE - 13))
    d.append('C%.2f %.2f %.2f %.2f %.2f %.2f'
             % (CX - 18, Y_BASE - 13, CX - 24, Y_BASE, xg + 20, Y_BASE))
    d.append('C%.2f %.2f %.2f %.2f %.2f %.2f'
             % (xg + 8, Y_BASE, xg, Y_BASE - 4, gauche[0][0], gauche[0][1]))
    d.append(_catmull(gauche))
    d.append('Z')
    return ' '.join(d)


def chemin_reflet(fraction=0.52, y_haut=118.0, y_bas=546.0):
    """Le reflet speculaire, tire du profil lui-meme.

    Il etait ecrit a la main en coordonnees fixes. Un reflet en dur ne suit
    pas la silhouette : au premier changement de profil il traversait la
    taille et sortait du verre. Ici il vaut une fraction constante du rayon,
    donc il se resserre exactement ou la bouteille se resserre — et il ne
    peut plus mentir sur la forme.
    """
    pts = [(CX - fraction * h, y) for y, h in PROFIL
           if y_haut <= y <= y_bas]
    return 'M%.2f %.2f %s' % (pts[0][0], pts[0][1], _catmull(pts))


def _ombre_flanc(cote):
    """Le bord assombri d'un flanc : c'est ce qui donne le volume rond."""
    pts = _cote_droit()
    if cote == 'g':
        pts = [(CX - (x - CX), y) for x, y in pts]
    return 'M%.2f %.2f %s' % (pts[0][0], pts[0][1], _catmull(pts))


# Les teintes de liquide rencontrees pendant la construction d'une page.
# Le degrade correspondant est ecrit UNE FOIS par page, pas une fois par
# bouteille — voir defs_partagees().
_TEINTES = set()


def _slug(hexa):
    return hexa.lstrip('#').lower()


def defs_partagees():
    """Le contour, le flanc, le masque et les degrades — une seule fois.

    Une page de saveurs affiche seize bouteilles. Repeter le trace du corps
    seize fois, c'est 100 ko de chemins identiques dans un fichier qu'on
    demande par ailleurs d'etre rapide. Les references SVG sont valables dans
    tout le document : un `<use>` suffit, et le bloc peut vivre en fin de
    page — un id se resout au rendu, pas a la lecture.

    Appeler cette fonction VIDE la liste des teintes : elle est faite pour
    etre appelee une fois par page, au moment ou la page est assemblee.
    """
    global _TEINTES
    liq = ''.join(
        '<linearGradient id="amaro-liq-%s" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="%s" stop-opacity=".62"/>'
        '<stop offset="1" stop-color="%s" stop-opacity=".92"/>'
        '</linearGradient>' % (_slug(t), t, t) for t in sorted(_TEINTES))
    _TEINTES = set()
    return """<svg class="amaro-defs" width="0" height="0" aria-hidden="true"
     focusable="false" style="position:absolute;width:0;height:0;overflow:hidden">
  <defs>
    <path id="amaro-corps" d="%(corps)s"/>
    <path id="amaro-flanc" d="%(flanc)s"/>
    <clipPath id="amaro-clip" clipPathUnits="userSpaceOnUse">
      <use href="#amaro-corps" xlink:href="#amaro-corps"/>
    </clipPath>
    <linearGradient id="amaro-verre" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0"    stop-color="#000" stop-opacity=".20"/>
      <stop offset=".14"  stop-color="#000" stop-opacity=".04"/>
      <stop offset=".30"  stop-color="#fff" stop-opacity=".55"/>
      <stop offset=".46"  stop-color="#fff" stop-opacity=".10"/>
      <stop offset=".78"  stop-color="#000" stop-opacity=".05"/>
      <stop offset="1"    stop-color="#000" stop-opacity=".22"/>
    </linearGradient>
    <linearGradient id="amaro-cap" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0"   stop-color="#8E3457"/>
      <stop offset=".32" stop-color="#CB5F87"/>
      <stop offset=".62" stop-color="#8E3457"/>
      <stop offset="1"   stop-color="#6B2540"/>
    </linearGradient>
    %(liq)s
  </defs>
</svg>""" % dict(corps=chemin_corps(), flanc=chemin_profil_droit(), liq=liq)


def logo(taille=28, couleur='currentColor'):
    """La marque : le 8 de la bouteille, reduit a deux anneaux et une taille.

    Le meme dessin partout — en-tete, favicon, pied de page. Une marque qui
    change de trace d'une page a l'autre n'est plus une marque.
    """
    return (
        '<svg class="logo8" viewBox="0 0 48 72" width="%d" height="%d" '
        'aria-hidden="true" focusable="false">'
        '<path fill="none" stroke="%s" stroke-width="5" '
        'stroke-linecap="round" stroke-linejoin="round" '
        'd="M24 6c9 0 14 5.5 14 12.5S29 30 24 32c-5 2-16 5.5-16 14.5S15 66 '
        '24 66s16-9 16-19.5S29 34 24 32c-5-2-16-6.5-16-13.5S15 6 24 6z"/>'
        '</svg>' % (int(taille * 48 / 72.0), taille, couleur))


def bouteille(cle='natural', teinte='#8FC7D8', etiquette='AMARO',
              sous_etiquette='', hauteur=420, interactif=False,
              gazeuse=False):
    """Le rendu complet d'une bouteille.

    Le trace du corps n'est PAS recopie ici : il est reference par `<use>`
    depuis le bloc de defs_partagees(), ecrit une seule fois par page. Une
    page de saveurs porte seize bouteilles ; seize copies du meme chemin
    faisaient 100 ko de doublon dans une page qu'on demande rapide.

    `interactif` ajoute les identifiants dont le visualiseur 360 a besoin ;
    sans lui, le SVG est une image fixe et ne coute pas une ligne de script.
    """
    _TEINTES.add(teinte)
    uid = 'b-' + cle + ('-i' if interactif else '')
    largeur = int(round(hauteur * LARGEUR / float(HAUTEUR)))

    r_etq = rayon((Y_ETIQUETTE[0] + Y_ETIQUETTE[1]) / 2.0)
    y0, y1 = Y_ETIQUETTE

    # Le niveau du liquide : sous l'epaule, jamais jusqu'au col. Une bouteille
    # remplie a ras bord ne passe pas la ligne de bouchage.
    y_liquide = 132.0

    bulles = ''
    if gazeuse:
        pos = [(104, 300, 3.0), (132, 360, 2.2), (112, 430, 2.6),
               (140, 480, 1.8), (96, 500, 2.0), (150, 250, 1.9),
               (124, 540, 2.4), (104, 220, 1.7)]
        bulles = ''.join(
            '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff" '
            'opacity=".55"/>' % p for p in pos)

    def gid(nom):
        return ' id="%s-%s"' % (uid, nom) if interactif else ''

    def use(ref, attrs=''):
        return ('<use href="#%s" xlink:href="#%s"%s/>'
                % (ref, ref, (' ' + attrs) if attrs else ''))

    return """
<svg class="bouteille" viewBox="0 0 %(W)d %(H)d" width="%(w)d" height="%(h)d"
     role="img" aria-label="%(alt)s" data-uid="%(uid)s">
  <!-- L'ombre portee au sol : sans elle la bouteille flotte. Son rayon est
       celui du TALON, pas un chiffre rond : plus large que le pied, elle
       depasse de chaque cote et se lit comme un evasement de la bouteille
       elle-meme. Vu sur la premiere capture. -->
  <ellipse cx="%(cx).1f" cy="%(ysol).1f" rx="%(rsol).1f" ry="9"
           fill="#43172A" opacity=".11"/>

  <g clip-path="url(#amaro-clip)">
    <rect x="0" y="0" width="%(W)d" height="%(H)d" fill="#fff"/>
    <rect x="0" y="%(yliq).1f" width="%(W)d" height="%(H)d"
          fill="url(#amaro-liq-%(tslug)s)"/>
    <!-- la surface du liquide est une ellipse : vue de face, un cylindre
         rempli montre son menisque, pas un trait -->
    <ellipse cx="%(cx).1f" cy="%(yliq).1f" rx="%(rliq).1f" ry="7"
             fill="%(teinte)s" opacity=".38"/>
    %(bulles)s

    <!-- les deux coutures de moule, a ±90° de la face. Elles reprennent le
         MEME flanc que le contour, ecrase horizontalement : c'est exactement
         la projection d'une generatrice du cylindre. -->
    %(couture_d)s
    %(couture_g)s

    <!-- le panneau arriere : il n'apparait que quand la face s'en va -->
    <g%(id_dos)s class="etq-dos" opacity="0">
      <rect x="%(ex).1f" y="%(y0).1f" width="%(ew).1f" height="%(eh).1f"
            fill="#FFFFFF" opacity=".92"/>
      <rect x="%(ex).1f" y="%(y0).1f" width="%(ew).1f" height="3"
            fill="#CB5F87"/>
      <g fill="#8E3457" opacity=".55">
        <rect x="%(tx).1f" y="%(t0).1f" width="%(tw).1f" height="4" rx="2"/>
        <rect x="%(tx).1f" y="%(t1).1f" width="%(tw2).1f" height="4" rx="2"/>
        <rect x="%(tx).1f" y="%(t2).1f" width="%(tw).1f" height="4" rx="2"/>
        <rect x="%(tx).1f" y="%(t3).1f" width="%(tw3).1f" height="4" rx="2"/>
      </g>
    </g>

    <!-- l'etiquette de face, azimut 0 -->
    <g%(id_face)s class="etq-face">
      <rect x="%(ex).1f" y="%(y0).1f" width="%(ew).1f" height="%(eh).1f"
            fill="#FFFFFF" opacity=".94"/>
      <rect x="%(ex).1f" y="%(y0).1f" width="%(ew).1f" height="3"
            fill="%(teinte)s"/>
      <text x="%(cx).1f" y="%(ty).1f" text-anchor="middle"
            font-family="Helvetica Neue, Helvetica, Arial, sans-serif"
            font-size="21" letter-spacing="4.5" font-weight="600"
            fill="#43172A">%(etq)s</text>
      <text x="%(cx).1f" y="%(ty2).1f" text-anchor="middle"
            font-family="Helvetica Neue, Helvetica, Arial, sans-serif"
            font-size="10" letter-spacing="2.4" fill="#8E3457"
            opacity=".85">%(sous)s</text>
    </g>

    <!-- la matiere par-dessus tout : c'est elle qui fait le plastique -->
    <rect x="0" y="0" width="%(W)d" height="%(H)d" fill="url(#amaro-verre)"/>
    <!-- le reflet speculaire ne tourne PAS avec la bouteille : il appartient
         a la lampe, pas au produit. Son trace suit le profil (voir
         chemin_reflet) : il se resserre a la taille comme le verre. -->
    <path d="%(reflet)s" fill="none" stroke="#fff" stroke-width="9"
          stroke-linecap="round" opacity=".58"/>
  </g>

  %(contour)s

  <!-- bague de col et bouchon -->
  <rect x="%(bx).1f" y="%(cb).1f" width="%(bw).1f" height="%(bh).1f" rx="3"
        fill="#F4D2DE" stroke="#43172A" stroke-opacity=".22"/>
  <rect x="%(px).1f" y="%(ch).1f" width="%(pw).1f" height="%(pht).1f" rx="5"
        fill="url(#amaro-cap)"/>
  <g stroke="#43172A" stroke-opacity=".18" stroke-width="1">%(cannelures)s</g>
</svg>""" % dict(
        W=LARGEUR, H=HAUTEUR, w=largeur, h=hauteur, uid=uid, cx=CX,
        teinte=teinte, tslug=_slug(teinte),
        alt=(etiquette + ' ' + sous_etiquette).strip(),
        yliq=y_liquide, rliq=rayon(y_liquide) - 3, ysol=Y_BASE + 7,
        rsol=PROFIL[-1][1] - 6,
        bulles=bulles,
        contour=use('amaro-corps',
                    'fill="none" stroke="#43172A" stroke-width="1.6" '
                    'opacity=".30"'),
        couture_d=use('amaro-flanc',
                      '%s class="couture" fill="none" stroke="#43172A" '
                      'stroke-width="1.1" opacity=".16" '
                      'transform="translate(%.1f,0) scale(0.001,1) '
                      'translate(%.1f,0)"' % (gid('couture-d'), CX, -CX)),
        couture_g=use('amaro-flanc',
                      '%s class="couture" fill="none" stroke="#43172A" '
                      'stroke-width="1.1" opacity=".16" '
                      'transform="translate(%.1f,0) scale(-0.001,1) '
                      'translate(%.1f,0)"' % (gid('couture-g'), CX, -CX)),
        ex=CX - r_etq + 6, ew=2 * (r_etq - 6), y0=y0, eh=y1 - y0,
        ty=y0 + 42, ty2=y0 + 62,
        tx=CX - r_etq + 22, tw=2 * (r_etq - 22), tw2=2 * (r_etq - 22) * 0.72,
        tw3=2 * (r_etq - 22) * 0.55,
        t0=y0 + 20, t1=y0 + 32, t2=y0 + 44, t3=y0 + 56,
        etq=etiquette, sous=sous_etiquette, reflet=chemin_reflet(),
        bx=CX - BAGUE_DEMI, cb=CAP_BAS - 4, bw=2 * BAGUE_DEMI, bh=14,
        px=CX - CAP_DEMI, ch=CAP_HAUT, pw=2 * CAP_DEMI,
        pht=CAP_BAS - CAP_HAUT,
        cannelures=''.join(
            '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
            % (CX - CAP_DEMI + 4 + i * 4.2, CAP_HAUT + 6,
               CX - CAP_DEMI + 4 + i * 4.2, CAP_BAS - 5)
            for i in range(9)),
        id_face=gid('face'), id_dos=gid('dos'),
    )


def script_360(uid, r_etiquette):
    """Le visualiseur 360, en clair, sans dependance.

    La rotation est un ETAT, pas une animation : la molette, le doigt, la
    souris et le clavier ecrivent tous le meme angle, et une seule fonction
    redessine. Deux chemins de rendu, ce sont deux bouteilles qui finissent
    par ne plus etre d'accord.
    """
    return """
(function () {
  var svg = document.querySelector('[data-uid="%(uid)s"]');
  if (!svg) return;
  var face = document.getElementById('%(uid)s-face'),
      dos  = document.getElementById('%(uid)s-dos'),
      cd   = document.getElementById('%(uid)s-couture-d'),
      cg   = document.getElementById('%(uid)s-couture-g'),
      lect = document.getElementById('lecture-angle'),
      curseur = document.getElementById('curseur-angle');
  var CX = %(cx).1f, R = %(r).1f, a = 0, glisse = false, x0 = 0, a0 = 0;

  function cyl(el, azimut, ecrase) {
    // x = R sin(t+a) ; visible si cos(t+a) > 0. C'est toute la geometrie.
    var t = azimut + a, c = Math.cos(t), s = Math.sin(t);
    if (c <= 0.02) { el.setAttribute('opacity', '0'); return; }
    var k = ecrase ? c : (c < 0 ? -c : c);
    if (k < 0.001) k = 0.001;
    el.setAttribute('opacity', String(Math.min(1, c * 1.6)));
    el.setAttribute('transform',
      'translate(' + (CX + R * s) + ',0) scale(' + k + ',1) translate(' +
      (-CX) + ',0)');
  }

  function couture(el, azimut) {
    var t = azimut + a, c = Math.cos(t), s = Math.sin(t);
    // Le flanc est deja a x = CX + r(y) ; l'ecraser de sin(t) le place a
    // x = CX + r(y)·sin(t), c'est-a-dire sur la bonne generatrice.
    if (c <= 0) { el.setAttribute('opacity', '0'); return; }
    var k = s;
    if (Math.abs(k) < 0.001) k = k < 0 ? -0.001 : 0.001;
    el.setAttribute('opacity', String(0.18 * Math.min(1, c * 2)));
    el.setAttribute('transform',
      'translate(' + CX + ',0) scale(' + k + ',1) translate(' + (-CX) + ',0)');
  }

  function rendre() {
    while (a < 0) a += Math.PI * 2;
    a = a %% (Math.PI * 2);
    cyl(face, 0, true);
    cyl(dos, Math.PI, false);
    couture(cd, Math.PI / 2);
    couture(cg, -Math.PI / 2);
    var deg = Math.round(a * 180 / Math.PI) %% 360;
    if (lect) lect.textContent = deg + '\\u00B0';
    if (curseur && document.activeElement !== curseur) curseur.value = deg;
  }

  function pointe(e) { return e.touches ? e.touches[0].clientX : e.clientX; }

  svg.addEventListener('pointerdown', function (e) {
    glisse = true; x0 = pointe(e); a0 = a;
    svg.setPointerCapture && svg.setPointerCapture(e.pointerId);
    svg.classList.add('tourne');
  });
  svg.addEventListener('pointermove', function (e) {
    if (!glisse) return;
    a = a0 + (pointe(e) - x0) * 0.012;
    rendre();
  });
  ['pointerup', 'pointercancel', 'pointerleave'].forEach(function (n) {
    svg.addEventListener(n, function () {
      glisse = false; svg.classList.remove('tourne');
    });
  });

  // Le curseur EST la commande accessible : au clavier, une image qu'on fait
  // glisser ne se manipule pas. Il n'y a donc pas de « version clavier »
  // separee — il y a un seul controle, et la souris s'y branche.
  if (curseur) {
    curseur.addEventListener('input', function () {
      a = curseur.value * Math.PI / 180; rendre();
    });
  }
  rendre();
})();
""" % dict(uid=uid, cx=CX, r=r_etiquette)
