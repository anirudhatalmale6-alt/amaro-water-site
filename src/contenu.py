# -*- coding: utf-8 -*-
"""Tout le contenu du site AMARO, en un seul fichier.

C'est ICI qu'on change les textes, les saveurs, les formats et les marches.
Aucune de ces chaines n'est ecrite en dur dans page_amaro.py : une phrase
recopiee dans le HTML est une phrase qu'on oublie de traduire.

────────────────────────────────────────────────────────────────────────────
CE QUI EST VOLONTAIREMENT VIDE, ET POURQUOI
────────────────────────────────────────────────────────────────────────────
Une eau embouteillee est un produit REGLEMENTE. L'origine de l'eau, l'analyse
minerale, le pH, la liste d'ingredients, le tableau nutritionnel, le taux de
rPET, la recyclabilite, le poids de la bouteille : ce sont des mentions
d'etiquetage et des allegations. Elles se prouvent avec un bulletin d'analyse,
une fiche technique du souffleur, une attestation du fournisseur de resine.

Je n'en invente aucune. Chaque valeur inconnue est un champ VIDE et VISIBLE
sur la page — « a renseigner » — pas un chiffre plausible. Un chiffre
plausible se recopie sur une etiquette, part chez un distributeur, et devient
une declaration fausse que personne ne se rappelle avoir ecrite.

Les valeurs qui viennent du cahier des charges (formats, noms de saveurs,
matiere PET/rPET, signature de marque) sont reprises telles quelles : elles
sont du client.
"""

# ---------------------------------------------------------------------------
# Marque
# ---------------------------------------------------------------------------

MARQUE = 'AMARO'

# La signature ne se traduit pas : c'est une marque, elle s'ecrit pareil dans
# les deux versions du site.
SIGNATURE = 'Water. Reimagined.'

# Le nom de domaine n'est pas arrete. Les liens inter-pages sont relatifs, il
# n'y a donc rien a changer le jour ou il l'est — sauf cette constante, qui
# sert aux balises canoniques et au plan du site.
DOMAINE = ''            # a renseigner : ex. https://amaro-water.com

# ---------------------------------------------------------------------------
# Navigation. L'ordre est celui de l'arborescence du cahier des charges (16).
# ---------------------------------------------------------------------------

NAV = [
    ('index.html',        'Accueil',                'Home'),
    ('notre-eau.html',    'Notre eau',              'Our Water'),
    ('saveurs.html',      'Saveurs',                'Flavors'),
    ('bouteille.html',    'La bouteille 8',         'The 8 Bottle'),
    ('produits.html',     'Produits',               'Products'),
    ('durabilite.html',   'Durabilité',             'Sustainability'),
    ('marque.html',       'La marque',              'About'),
    ('business.html',     'AMARO Business',         'AMARO Business'),
    ('distribution.html', 'Distribution',           'Global Distribution'),
    ('actualites.html',   'Actualités',             'News'),
    ('contact.html',      'Contact',                'Contact'),
]

# Pages hors navigation principale : elles existent, elles sont liees depuis
# le pied de page, elles n'encombrent pas la barre du haut.
NAV_PIED = [
    ('boutique.html',     'Boutique',               'Shop'),
    ('design.html',       'Charte graphique',       'Design system'),
    ('a-renseigner.html', 'Ce qui reste à fournir', 'What is still needed'),
]

# ---------------------------------------------------------------------------
# Accueil
# ---------------------------------------------------------------------------

HERO = dict(
    titre_fr='Water. Reimagined.',
    titre_en='Water. Reimagined.',
    chapo_fr='Une eau embouteillée et des eaux aromatisées, dans une '
             'bouteille dessinée comme un 8.',
    chapo_en='Bottled water and flavored waters, in a bottle drawn as '
             'a figure 8.',
    cta1_fr='Découvrir AMARO', cta1_en='Discover AMARO',
    cta2_fr='Devenir distributeur', cta2_en='Become a Distributor',
)

# Les cinq stations de la navigation verticale de l'accueil (cahier, 3).
STATIONS = [
    dict(cle='bouteille', lien='bouteille.html',
         num='01',
         titre_fr='La bouteille signature',
         titre_en='The signature bottle',
         texte_fr='Deux volumes ronds, une taille resserrée au milieu. '
                  'La silhouette dessine un 8 et se tient d’une main.',
         texte_en='Two round volumes, a narrow waist between them. The '
                  'silhouette draws a figure 8 and sits in one hand.'),
    dict(cle='naturelle', lien='notre-eau.html',
         num='02',
         titre_fr='Les eaux naturelles',
         titre_en='The natural waters',
         texte_fr='AMARO Natural, plate. AMARO Sparkling, gazeuse. '
                  'Quatre formats, du 330 ml au 1,5 L.',
         texte_en='AMARO Natural, still. AMARO Sparkling, sparkling. '
                  'Four formats, from 330 ml to 1.5 L.'),
    dict(cle='saveurs', lien='saveurs.html',
         num='03',
         titre_fr='Les eaux aromatisées',
         titre_en='The flavored waters',
         texte_fr='Huit saveurs. Une même bouteille, un code couleur par '
                  'saveur, une identité qui ne bouge pas.',
         texte_en='Eight flavors. One bottle, one color code per flavor, '
                  'one identity that never moves.'),
    dict(cle='engagements', lien='durabilite.html',
         num='04',
         titre_fr='Les engagements',
         titre_en='The commitments',
         texte_fr='Allègement, recyclabilité, rPET, logistique. Ce qui sera '
                  'publié devra être prouvé.',
         texte_en='Lightweighting, recyclability, rPET, logistics. What gets '
                  'published will have to be proven.'),
    dict(cle='reseau', lien='distribution.html',
         num='05',
         titre_fr='Le réseau de distribution',
         titre_en='The distribution network',
         texte_fr='Marchés ouverts, marchés à ouvrir. AMARO cherche des '
                  'partenaires.',
         texte_en='Open markets, markets to open. AMARO is looking for '
                  'partners.'),
]

# ---------------------------------------------------------------------------
# Notre eau — AMARO Natural / AMARO Sparkling
#
# Les FORMATS viennent du cahier des charges (4). Tout le reste — origine,
# analyse, pH, conditionnement — est un fait d'etiquetage : vide et visible.
# ---------------------------------------------------------------------------

FORMATS = ['330 ml', '500 ml', '1 L', '1,5 L']
FORMATS_EN = ['330 ml', '500 ml', '1 L', '1.5 L']

EAUX = [
    dict(cle='natural', nom='AMARO Natural',
         type_fr='Eau plate', type_en='Still water',
         teinte='#8FC7D8',
         texte_fr='L’eau AMARO dans sa forme la plus simple. Rien d’ajouté, '
                  'rien de retiré au-delà de ce que la réglementation du '
                  'marché impose.',
         texte_en='AMARO water at its plainest. Nothing added, nothing '
                  'removed beyond what the market’s regulations require.'),
    dict(cle='sparkling', nom='AMARO Sparkling',
         type_fr='Eau gazeuse', type_en='Sparkling water',
         teinte='#B8D4E0',
         texte_fr='La même eau, gazéifiée. Bulle fine, destinée à la table '
                  'et à la restauration.',
         texte_en='The same water, carbonated. Fine bubble, made for the '
                  'table and for food service.'),
]

# Les lignes de la fiche technique d'une eau. `valeur` vide = affiche
# « à renseigner » en clair sur la page.
FICHE_EAU = [
    ('origine',       'Origine de l’eau',            'Water source',            ''),
    ('type_legal',    'Dénomination légale',         'Legal denomination',      ''),
    ('analyse',       'Analyse minérale (mg/L)',     'Mineral analysis (mg/L)', ''),
    ('ph',            'pH',                          'pH',                      ''),
    ('traitement',    'Traitements autorisés',       'Authorized treatments',   ''),
    ('mentions',      'Mentions réglementaires',     'Regulatory statements',   ''),
    ('conditionnement', 'Conditionnement (colis, palette)',
                        'Case pack (carton, pallet)',                           ''),
    ('dlc',           'Durée de conservation',       'Shelf life',              ''),
    ('gtin',          'Code GTIN / EAN',             'GTIN / EAN code',         ''),
]

# ---------------------------------------------------------------------------
# Saveurs. Les huit noms viennent du cahier des charges (5).
#
# La description sensorielle, je l'ecris : c'est de la copie, pas un fait.
# Les ingredients et le tableau nutritionnel, non : ce sont des mentions
# d'etiquetage, elles viennent du formulateur.
# ---------------------------------------------------------------------------

SAVEURS = [
    dict(cle='lemon', nom='Lemon',
         fr='Citron', teinte='#E9D14A',
         d_fr='Le plus franc des huit. Zeste net, attaque courte, rien qui '
              'traîne en bouche.',
         d_en='The most direct of the eight. Clean zest, short attack, '
              'nothing lingering.'),
    dict(cle='lime', nom='Lime',
         fr='Citron vert', teinte='#A8CE4C',
         d_fr='Plus vert et plus sec que le citron. Se tient bien froid, '
              'très froid.',
         d_en='Greener and drier than lemon. Holds up cold, very cold.'),
    dict(cle='mint', nom='Mint',
         fr='Menthe', teinte='#6FC4A0',
         d_fr='Une fraîcheur de fin de repas, sans sucrosité apparente.',
         d_en='An after-meal freshness, with no apparent sweetness.'),
    dict(cle='strawberry', nom='Strawberry',
         fr='Fraise', teinte='#E2607E',
         d_fr='La saveur d’entrée du rayon. Ronde, immédiatement lisible.',
         d_en='The gateway flavor of the shelf. Round, immediately legible.'),
    dict(cle='peach', nom='Peach',
         fr='Pêche', teinte='#F0A46A',
         d_fr='Douce et veloutée. La saveur qui marche partout, y compris '
              'là où les agrumes ne prennent pas.',
         d_en='Soft and velvety. The flavor that travels, including where '
              'citrus does not.'),
    dict(cle='orange', nom='Orange',
         fr='Orange', teinte='#EE8B3C',
         d_fr='Plus large que le citron, plus solaire. Un classique de '
              'petit-déjeuner porté sur l’eau.',
         d_en='Wider than lemon, sunnier. A breakfast classic carried over '
              'to water.'),
    dict(cle='berries', nom='Berries',
         fr='Fruits rouges', teinte='#B84A72',
         d_fr='L’assemblage. Couleur profonde, la plus visible en linéaire.',
         d_en='The blend. Deep color, the most visible one on shelf.'),
    dict(cle='cucumber', nom='Cucumber & Mint',
         fr='Concombre & menthe', teinte='#7EC28C',
         d_fr='La plus adulte. Végétale, peu sucrée en perception, taillée '
              'pour l’hôtellerie et les salles de sport.',
         d_en='The most grown-up. Vegetal, low in perceived sweetness, cut '
              'for hospitality and gyms.'),
]

FICHE_SAVEUR = [
    ('ingredients',   'Liste d’ingrédients',         'Ingredients list',        ''),
    ('nutrition',     'Tableau nutritionnel (100 ml)',
                      'Nutrition table (per 100 ml)',                           ''),
    ('sucres',        'Sucres / édulcorants',        'Sugars / sweeteners',     ''),
    ('allergenes',    'Allergènes',                  'Allergens',               ''),
    ('mentions',      'Mentions réglementaires',     'Regulatory statements',   ''),
    ('conditionnement', 'Conditionnement (colis, palette)',
                        'Case pack (carton, pallet)',                           ''),
    ('dlc',           'Durée de conservation',       'Shelf life',              ''),
    ('gtin',          'Code GTIN / EAN',             'GTIN / EAN code',         ''),
]

# ---------------------------------------------------------------------------
# La bouteille AMARO 8
# ---------------------------------------------------------------------------

BOUTEILLE_INTRO_FR = (
    'La bouteille AMARO n’est pas un cylindre avec une étiquette dessus. '
    'Sa silhouette est le produit : deux volumes arrondis reliés par une '
    'zone centrale plus étroite, qui dessinent un 8 de profil et servent de '
    'prise en main.')
BOUTEILLE_INTRO_EN = (
    'The AMARO bottle is not a cylinder with a label on it. Its silhouette '
    'is the product: two rounded volumes joined by a narrower central zone, '
    'drawing a figure 8 in profile and doubling as the grip.')

# Les six contraintes que le dessin doit concilier (cahier, 6).
CONTRAINTES = [
    ('Identité', 'Identity',
     'Reconnaissable en rayon, de loin, sans lire l’étiquette.',
     'Recognisable on shelf, from a distance, without reading the label.'),
    ('Ergonomie', 'Ergonomics',
     'La taille resserrée tombe sous les doigts. C’est la prise, pas un '
     'ornement.',
     'The narrow waist falls under the fingers. It is the grip, not an '
     'ornament.'),
    ('Stabilité', 'Stability',
     'Base large et plate : le centre de gravité reste bas malgré le '
     'volume haut.',
     'Wide flat base: the centre of gravity stays low despite the upper '
     'volume.'),
    ('Résistance', 'Strength',
     'La zone étroite est la plus sollicitée. Elle est nervurée et son '
     'épaisseur est un point de validation.',
     'The narrow zone takes the most load. It is ribbed, and its wall '
     'thickness is a validation point.'),
    ('Légèreté', 'Lightweighting',
     'Moins de matière par bouteille, à condition de tenir la palette. Le '
     'poids se fixe à l’essai, pas sur le papier.',
     'Less material per bottle, provided the pallet holds. Weight is set '
     'on trial, not on paper.'),
    ('Ligne industrielle', 'Industrial line',
     'Soufflage, remplissage, bouchage, étiquetage, palettisation : la '
     'forme doit passer les cinq.',
     'Blowing, filling, capping, labelling, palletising: the shape has to '
     'clear all five.'),
]

# Fiche technique de la bouteille. TOUT est vide : ces valeurs sortent du
# souffleur et du fournisseur de resine, pas de moi.
FICHE_BOUTEILLE = [
    ('matiere',    'Matière',                     'Material',
     'PET / rPET alimentaire'),   # vient du cahier des charges (6)
    ('rpet',       'Taux de rPET',                'rPET content',            ''),
    ('poids',      'Poids de la préforme (g)',    'Preform weight (g)',      ''),
    ('col',        'Norme de col / bouchon',      'Neck finish / closure',   ''),
    ('hauteur',    'Hauteur hors tout (mm)',      'Overall height (mm)',     ''),
    ('diametre',   'Diamètre maximal (mm)',       'Maximum diameter (mm)',   ''),
    ('taille',     'Diamètre à la taille (mm)',   'Waist diameter (mm)',     ''),
    ('epaisseur',  'Épaisseur mini de paroi (mm)',
                   'Minimum wall thickness (mm)',                            ''),
    ('topload',    'Résistance à la compression', 'Top load resistance',     ''),
    ('etiquette',  'Type d’étiquette',            'Label type',              ''),
    ('palette',    'Colisage et palettisation',   'Case and pallet pattern', ''),
    ('moule',      'Fabricant du moule',          'Mould maker',             ''),
]

# ---------------------------------------------------------------------------
# Durabilite. Ce sont des CHANTIERS, pas des resultats.
# ---------------------------------------------------------------------------

DURABILITE_AVERTISSEMENT_FR = (
    'Aucun chiffre n’est publié sur cette page tant qu’il n’est pas '
    'vérifiable. Une allégation environnementale — « recyclable », '
    '« x % recyclé », « neutre » — est encadrée par la réglementation du '
    'marché où elle est publiée, et se prouve avec une pièce. Les emplacements '
    'ci-dessous attendent ces pièces.')
DURABILITE_AVERTISSEMENT_EN = (
    'No figure is published on this page until it is verifiable. An '
    'environmental claim — “recyclable”, “x % recycled”, “neutral” — is '
    'governed by the regulations of the market where it is published, and is '
    'proven with a document. The slots below are waiting for those documents.')

ENGAGEMENTS = [
    ('Allègement', 'Lightweighting',
     'Réduire la matière par bouteille sans perdre la tenue en palette.',
     'Reduce material per bottle without losing pallet performance.',
     ''),
    ('Recyclabilité', 'Recyclability',
     'Bouteille, bouchon et étiquette compatibles avec les filières des '
     'marchés visés.',
     'Bottle, cap and label compatible with the recycling streams of the '
     'target markets.',
     ''),
    ('rPET', 'rPET',
     'Intégrer du PET recyclé de qualité alimentaire là où la réglementation '
     'et l’approvisionnement le permettent.',
     'Use food-grade recycled PET where regulation and supply allow.',
     ''),
    ('Logistique', 'Logistics',
     'Optimiser le remplissage des palettes et des conteneurs : moins de '
     'vide transporté.',
     'Optimise pallet and container fill: less air shipped.',
     ''),
    ('Déchets', 'Waste',
     'Réduire les rebuts de production et les réintégrer.',
     'Reduce production scrap and feed it back in.',
     ''),
    ('Énergie', 'Energy',
     'Suivre la consommation par hectolitre produit, site par site.',
     'Track consumption per hectolitre produced, site by site.',
     ''),
]

# ---------------------------------------------------------------------------
# La marque. Histoire, vision, ambition — sans inventer de date, de fondateur
# ni de siege social.
# ---------------------------------------------------------------------------

MARQUE_VISION_FR = (
    'AMARO est une marque d’eau et d’hydratation à vocation internationale. '
    'Le positionnement est moderne et premium, et la gamme est construite '
    'pour s’élargir : ce qui est vrai de l’eau plate doit rester vrai de ce '
    'qui viendra après.')
MARQUE_VISION_EN = (
    'AMARO is an international water and hydration brand. The positioning is '
    'modern and premium, and the range is built to widen: what holds true '
    'for still water has to keep holding for whatever comes next.')

FICHE_SOCIETE = [
    ('raison',   'Raison sociale',              'Legal entity',            ''),
    ('siege',    'Siège social',                'Head office',             ''),
    ('immat',    'Numéro d’immatriculation',    'Registration number',     ''),
    ('creation', 'Année de création',           'Year founded',            ''),
    ('dirigeant', 'Direction',                  'Leadership',              ''),
    ('sites',    'Sites de production',         'Production sites',        ''),
]

# ---------------------------------------------------------------------------
# Business B2B. Les champs du formulaire viennent du cahier des charges (8).
# ---------------------------------------------------------------------------

SECTEURS = [
    ('distributeur', 'Distributeur', 'Distributor'),
    ('grossiste',    'Grossiste', 'Wholesaler'),
    ('supermarche',  'Supermarché / retail', 'Supermarket / retail'),
    ('hotel',        'Hôtellerie', 'Hotels'),
    ('restaurant',   'Restauration', 'Restaurants'),
    ('cafe',         'Cafés', 'Cafés'),
    ('sport',        'Salles de sport', 'Gyms'),
    ('entreprise',   'Entreprises', 'Corporate'),
    ('evenement',    'Événementiel', 'Events'),
    ('autre',        'Autre', 'Other'),
]

VOLUMES = [
    ('', 'Volume estimé', 'Estimated volume'),
    ('palette',   'Moins d’une palette / mois', 'Less than one pallet / month'),
    ('palettes',  '1 à 10 palettes / mois', '1 to 10 pallets / month'),
    ('camion',    'Camion complet', 'Full truck'),
    ('conteneur', 'Conteneur complet', 'Full container'),
    ('inconnu',   'À déterminer', 'To be determined'),
]

# ---------------------------------------------------------------------------
# Distribution internationale.
#
# LA LISTE EST VIDE, ET C'EST VOULU. Ecrire « AMARO est disponible en France »
# ou meme « AMARO cherche un distributeur au Bresil » est une declaration
# commerciale : elle engage la marque devant des gens qui vont la lire et
# ecrire. Elle vient du client, pas de moi.
#
# Pour la remplir : une ligne par marche, statut parmi 'available',
# 'wanted', 'soon'. La page, la carte, le compteur et les filtres se mettent
# a jour tout seuls.
#
#     MARCHES = [
#         ('Canada', 'Canada', 'Amérique du Nord', 'North America', 'available'),
#         ('France', 'France', 'Europe', 'Europe', 'wanted'),
#     ]
# ---------------------------------------------------------------------------

MARCHES = []

STATUTS = [
    ('available', 'Disponible',           'Available',         '#3F9F72'),
    ('wanted',    'Distributeur recherché', 'Distributor Wanted', '#CB5F87'),
    ('soon',      'Bientôt',              'Coming Soon',       '#9A8FA6'),
]

REGIONS = [
    ('Europe', 'Europe'),
    ('Amérique du Nord', 'North America'),
    ('Amérique latine', 'Latin America'),
    ('Moyen-Orient', 'Middle East'),
    ('Afrique', 'Africa'),
    ('Asie', 'Asia'),
    ('Océanie', 'Oceania'),
]

# ---------------------------------------------------------------------------
# Actualites. Vide, et la page le dit.
# ---------------------------------------------------------------------------

ACTUALITES = []

# ---------------------------------------------------------------------------
# Contact. Rien d'invente : ni adresse, ni telephone, ni courriel.
# ---------------------------------------------------------------------------

CONTACT = [
    ('adresse',  'Adresse',            'Address',          ''),
    ('tel',      'Téléphone',          'Phone',            ''),
    ('courriel', 'Courriel commercial', 'Sales e-mail',    ''),
    ('presse',   'Contact presse',     'Press contact',    ''),
    ('horaires', 'Horaires',           'Opening hours',    ''),
]

RESEAUX = [
    ('instagram', 'Instagram', ''),
    ('linkedin',  'LinkedIn',  ''),
    ('facebook',  'Facebook',  ''),
]

# ---------------------------------------------------------------------------
# Charte graphique : rose et blanc.
#
# Le client a demande « rose et blanc ». Une marque ne tient pas sur deux
# couleurs : il en faut une echelle, sinon chaque page reinvente son rose et
# la marque se delave. Voici l'echelle. Le blanc et l'encre en font partie.
# ---------------------------------------------------------------------------

ROSE = [
    ('rose-50',  '#FDF6F8', 'Fond de page, blanc rosé'),
    ('rose-100', '#FAE9EF', 'Fond de section'),
    ('rose-200', '#F4D2DE', 'Filets, bordures, aplats doux'),
    ('rose-300', '#EAB2C6', 'Aplats, survols'),
    ('rose-400', '#DC8CAA', 'Illustration, dégradés'),
    ('rose-500', '#CB5F87', 'ROSE AMARO — la couleur de marque. Aplats, '
                            'graphisme, gros titres'),
    ('rose-600', '#B04670', 'LE ROSE DU TEXTE. Boutons, surtitres, liens : '
                            'rose-500 sur blanc ne donne que 4,05 pour 1'),
    ('rose-700', '#8E3457', 'Titres sur fond clair'),
    ('rose-800', '#6B2540', 'Texte accentué'),
    ('rose-900', '#43172A', 'Encre — le texte courant'),
]

NEUTRES = [
    ('blanc',    '#FFFFFF', 'Blanc pur — la deuxième couleur de la marque'),
    ('gris-100', '#F4F1F2', 'Gris rosé très clair'),
    ('gris-400', '#A9A0A4', 'Texte secondaire'),
    ('gris-700', '#544A4E', 'Texte sur fond clair, alternative à l’encre'),
]

# ---------------------------------------------------------------------------
# Le releve des trous. Rempli automatiquement au moment de la construction
# par page_amaro.py — il n'est PAS tenu a la main, sinon il se desynchronise
# du site le jour ou une valeur est remplie.
# ---------------------------------------------------------------------------

def champs_vides():
    """Toutes les lignes de fiche laissees vides, avec leur page.

    Sert a deux choses : la page « ce qui reste a fournir », et le test qui
    verifie qu'aucun de ces champs n'a ete rempli par erreur avec une valeur
    inventee.
    """
    trous = []
    tables = [
        ('notre-eau.html',  'Fiche technique des eaux',
         'Water technical sheet',       FICHE_EAU),
        ('saveurs.html',    'Fiche technique des saveurs',
         'Flavor technical sheet',      FICHE_SAVEUR),
        ('bouteille.html',  'Fiche technique de la bouteille',
         'Bottle technical sheet',      FICHE_BOUTEILLE),
        ('marque.html',     'Identité de la société',
         'Company identity',            FICHE_SOCIETE),
        ('contact.html',    'Coordonnées',
         'Contact details',             CONTACT),
    ]
    for page, gfr, gen, table in tables:
        for cle, fr, en, val in table:
            if not val:
                trous.append(dict(page=page, groupe_fr=gfr, groupe_en=gen,
                                  cle=cle, fr=fr, en=en))
    for fr, en, dfr, den, val in ENGAGEMENTS:
        if not val:
            # Le prefixe « durabilite- » est celui que la page ecrit dans
            # data-vide. Il etait absent ici, et le controle qui compare les
            # deux tombait : la declaration et le rendu se donnaient deux
            # noms differents pour la meme chose.
            trous.append(dict(page='durabilite.html',
                              groupe_fr='Engagements — chiffre à prouver',
                              groupe_en='Commitments — figure to prove',
                              cle='durabilite-' + fr, fr=fr, en=en))
    return trous
