# -*- coding: utf-8 -*-
"""Captures du site AMARO.

Deux regles tenues ici :

  - la fenetre fait 1280x720 et on ne capture QUE ce qu'elle montre. Une
    capture pleine page d'un site a longues sections depasse les 2000 px et
    devient inenvoyable ;
  - avant chaque capture on attend que les apparitions au defilement soient
    jouees, sinon on photographie un bloc a mi-transition et on livre une
    page qui a l'air cassee alors qu'elle ne l'est pas.

    python3 captures-amaro.py [port]
"""

import os
import sys

from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8807
BASE = 'http://127.0.0.1:%d/' % PORT

# (fichier, page, y de defilement, langue, largeur, hauteur, action)
VUES = [
    ('am-01-accueil.png',      'index.html',        0,    'fr', 1280, 720, None),
    ('am-02-stations.png',     'index.html',        820,  'fr', 1280, 720, None),
    ('am-03-gamme.png',        'index.html',        1560, 'fr', 1280, 720, None),
    ('am-04-bouteille.png',    'bouteille.html',    420,  'fr', 1280, 720, None),
    ('am-05-bouteille-180.png', 'bouteille.html',   420,  'fr', 1280, 720, 'tourner'),
    ('am-06-contraintes.png',  'bouteille.html',    980,  'fr', 1280, 720, None),
    ('am-07-saveurs.png',      'saveurs.html',      250,  'fr', 1280, 720, None),
    ('am-08-fiche-saveur.png', 'saveurs.html',      0,    'fr', 1280, 720, 'ouvrir'),
    ('am-09-eau.png',          'notre-eau.html',    150,  'fr', 1280, 720, None),
    ('am-10-produits.png',     'produits.html',     200,  'fr', 1280, 720, None),
    ('am-11-filtre.png',       'produits.html',     200,  'fr', 1280, 720, 'filtrer'),
    ('am-12-business.png',     'business.html',     130,  'fr', 1280, 720, None),
    ('am-13-form-erreurs.png', 'business.html',     130,  'fr', 1280, 720, 'valider'),
    ('am-14-distribution.png', 'distribution.html', 100,  'fr', 1280, 720, None),
    ('am-15-durabilite.png',   'durabilite.html',   140,  'fr', 1280, 720, None),
    ('am-16-charte.png',       'design.html',       150,  'fr', 1280, 720, None),
    ('am-17-charte-saveurs.png', 'design.html',     1750, 'fr', 1280, 720, None),
    ('am-18-a-renseigner.png', 'a-renseigner.html', 120,  'fr', 1280, 720, None),
    ('am-19-anglais.png',      'index.html',        0,    'en', 1280, 720, None),
    ('am-20-anglais-saveurs.png', 'saveurs.html',   250,  'en', 1280, 720, None),
    ('am-21-mobile.png',       'index.html',        0,    'fr', 390,  760, None),
    ('am-22-mobile-saveurs.png', 'saveurs.html',    120,  'fr', 390,  760, None),
    ('am-23-mobile-form.png',  'business.html',     220,  'fr', 390,  760, None),
]


def poser(page, y, langue, action):
    if langue == 'en':
        page.click('[data-langue="en"]')
        page.wait_for_timeout(120)
    if action == 'tourner':
        page.evaluate("""() => {
            const c = document.getElementById('curseur-angle');
            c.value = 168;
            c.dispatchEvent(new Event('input', {bubbles: true}));
        }""")
        page.wait_for_timeout(150)
    if action == 'ouvrir':
        page.evaluate("""() => {
            const d = document.querySelectorAll('details.detail')[3];
            d.open = true;
            d.scrollIntoView({block: 'center'});
        }""")
        page.wait_for_timeout(220)
        return
    if action == 'filtrer':
        page.click('#filtres input[value="aromatisee"]')
        page.wait_for_timeout(160)
    if action == 'valider':
        page.click('#b2b button[type="submit"]')
        page.wait_for_timeout(160)
    page.evaluate('window.scrollTo(0, %d)' % y)
    # On laisse les apparitions se terminer : capturer a mi-transition, c'est
    # livrer une page qui a l'air cassee alors qu'elle ne l'est pas.
    page.wait_for_timeout(900)


def main():
    sortie = ICI
    with sync_playwright() as p:
        nav = p.chromium.launch(args=['--disable-lcd-text',
                                      '--force-color-profile=srgb'])
        for nom, url, y, langue, w, h, action in VUES:
            ctx = nav.new_context(viewport={'width': w, 'height': h},
                                  device_scale_factor=1,
                                  is_mobile=(w < 500))
            page = ctx.new_page()
            page.goto(BASE + url, wait_until='networkidle')
            page.wait_for_timeout(250)
            poser(page, y, langue, action)
            chemin = os.path.join(sortie, nom)
            page.screenshot(path=chemin)
            print('%-30s %5d x %-5d %7d o' % (nom, w, h,
                                              os.path.getsize(chemin)))
            ctx.close()
        nav.close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
