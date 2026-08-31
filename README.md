# AMARO — site web

Eau embouteillée et eaux aromatisées. Bouteille signature en PET/rPET dont la
silhouette dessine un 8.

Quatorze pages, deux langues (FR/EN), rose et blanc. Tout est généré par des
scripts Python et sort en HTML/CSS/JS statique : aucune base de données,
aucune dépendance, aucun appel à un service extérieur. Le dossier `demo/` se
dépose tel quel dans un `public_html` et il tourne.

---

## Ce qui est en place

| Page | Fichier | Section du cahier des charges |
|---|---|---|
| Accueil | `index.html` | 3 |
| Notre eau | `notre-eau.html` | 4 |
| Saveurs | `saveurs.html` | 5 |
| La bouteille 8 | `bouteille.html` | 6 |
| Produits | `produits.html` | 7 |
| AMARO Business | `business.html` | 8 |
| Distribution | `distribution.html` | 9 |
| Durabilité | `durabilite.html` | 10 |
| La marque | `marque.html` | 11 |
| Boutique | `boutique.html` | 12 |
| Actualités | `actualites.html` | 16 |
| Contact | `contact.html` | 16 |
| Charte graphique | `design.html` | 13, 17 |
| Ce qui reste à fournir | `a-renseigner.html` | — |

Plus : responsive, bilingue, SEO de base, formulaire B2B validé des deux
côtés, filtres de catalogue, visualiseur 360° de la bouteille, et un
traitement serveur du formulaire (`formulaire.php`) prêt à brancher.

---

## Les valeurs volontairement vides — 45 champs

C'est le point le plus important de ce dépôt, alors il est en haut.

Une eau embouteillée est un produit **réglementé**. L'origine de l'eau,
l'analyse minérale, le pH, la dénomination légale, la liste d'ingrédients, le
tableau nutritionnel, les allergènes, le taux de rPET, la recyclabilité, le
poids de préforme, la résistance à la compression, le colisage, le GTIN : ce
sont des mentions d'étiquetage et des allégations. Chacune se prouve avec une
pièce — bulletin d'analyse de laboratoire, fiche technique du souffleur,
attestation du fournisseur de résine.

**Je n'en invente aucune.** Chaque valeur inconnue s'affiche sur la page
publique comme une pastille « à renseigner », visible, qui se compte et se
réclame. Pas un tiret discret : un tiret se lit comme « sans objet » et
disparaît dans la page.

La raison est simple. Un chiffre plausible écrit ici finit recopié sur une
étiquette, part chez un distributeur, et devient une déclaration fausse que
personne ne se rappelle avoir écrite.

La page `a-renseigner.html` liste les 45 champs, groupés, avec un lien vers la
page où chacun se trouve. **Cette liste est calculée à la construction** : elle
ne peut pas se désynchroniser du site. Le jour où une valeur est remplie, elle
disparaît de la liste toute seule.

Même règle pour la page Durabilité : aucune allégation environnementale
chiffrée n'est publiée. Une allégation « recyclable », « x % recyclé »,
« neutre » est encadrée par la réglementation du marché où elle est publiée.
Les six engagements sont présentés comme des **chantiers**, avec un
emplacement vide pour l'indicateur.

Et rien n'est inventé non plus sur `marque.html` (raison sociale, siège,
année de création, direction) ni sur `contact.html` (adresse, téléphone,
courriel). Un contact inventé sur un site B2B se compose, et tombe dans le
vide devant un distributeur.

---

## La bouteille AMARO 8

`bouteille.py` dessine la bouteille en SVG à partir d'un **profil de rayons** :
une liste de couples (hauteur, demi-largeur). Le contour, la matière, le
liquide, le reflet, les coutures de moule et l'étiquette en découlent tous.
Changer la forme = changer `PROFIL`, rien d'autre.

Trois propriétés du dessin, à préserver si le profil est retouché :

- la **taille** est à 38 contre 92 au plus large, soit 41 %. C'est le
  pincement qui fait le 8 ;
- les **deux lobes sont convexes d'un bout à l'autre**. Un seul palier de
  largeur constante et la silhouette se lit comme un cylindre ;
- le **pied revient vers l'intérieur** (92 au ventre bas, 61 au talon). Sans
  ce retrait, le lobe du bas n'a pas de bas et le 8 redevient une poire.

### Ce que c'est, et ce que ce n'est pas

C'est un **rendu vectoriel que je dessine**. Ce n'est pas une photographie et
pas un décalque : la bouteille n'est pas fabriquée. La page le dit en clair.
Le jour où elle existe, la photo remplace le rendu et la page ne change pas.

### Le 360°

Une bouteille de section circulaire a la **même silhouette sous tous les
angles** : la faire tourner ne change pas son contour, ça change ce qui est
écrit dessus. Le visualiseur applique donc la vraie géométrie du cylindre :

    un point à l'azimut t, sur un rayon r, se projette en x = r·sin(t + a)
    et n'est visible que si cos(t + a) > 0

L'étiquette de face glisse en `r·sin(a)` et s'écrase en `cos(a)` ; le panneau
arrière apparaît exactement quand la face disparaît ; les deux coutures de
moule balaient le corps. C'est un vrai tour, pas un fondu entre deux images —
et `tests-amaro.py` le vérifie **numériquement**, angle par angle, contre la
formule.

Le curseur est la commande : à la souris on fait glisser la bouteille, au
clavier on utilise le curseur, et les deux écrivent le même état.

---

## Rose et blanc

La couleur demandée était « rose et blanc ». Deux couleurs ne suffisent pas à
tenir un site : il en faut une échelle, sinon chaque page réinvente son rose
et la marque se délave d'un écran à l'autre. L'échelle est déclarée une seule
fois (`ROSE` et `NEUTRES` dans `contenu.py`), et `design.html` la montre telle
quelle — cette page **lit** la palette, elle ne la recopie pas.

**La règle qui compte : rose-500 (`#CB5F87`) est la couleur de marque, ce
n'est pas la couleur du texte.** Mesuré sur blanc il donne 4,05 pour 1, sous
le seuil de 4,5. Les boutons, surtitres et liens utilisent donc rose-600
(`#B04670`, 5,7 pour 1). Rose-500 reste sur les aplats, le graphisme et les
très gros titres, où le seuil est de 3.

Le code couleur des saveurs ne touche pas au chrome de la marque : la saveur
ne colore que le liquide de la bouteille et un filet de 3 px. C'est ce qui
permet huit codes distincts sans huit identités.

---

## Construire

```
python3 page_amaro.py          # écrit les 14 pages + styles.css + script.js dans demo/
python3 tests-amaro.py 8807    # 97 contrôles sur les pages rendues
python3 captures-amaro.py 8807 # 23 captures 1280x720 et 390x760
```

Les deux derniers ont besoin d'un serveur local :

```
cd demo && python3 -m http.server 8807
```

---

## Remplir ce qui manque

Tout se passe dans `contenu.py`, puis on relance `python3 page_amaro.py`.

**Les marchés** (`MARCHES`) — la liste est vide, et c'est voulu : écrire
« AMARO est disponible ici » ou « AMARO cherche un distributeur là » est une
déclaration commerciale. Une ligne par marché ; la page, la légende et les
compteurs se remplissent seuls.

```python
MARCHES = [
    ('Canada', 'Canada', 'Amérique du Nord', 'North America', 'available'),
    ('France', 'France', 'Europe',           'Europe',        'wanted'),
    ('Maroc',  'Morocco', 'Afrique',         'Africa',        'soon'),
]
```

Statuts possibles : `available`, `wanted`, `soon`.

**Les actualités** (`ACTUALITES`), **les fiches techniques** (`FICHE_EAU`,
`FICHE_SAVEUR`, `FICHE_BOUTEILLE`), **la société** (`FICHE_SOCIETE`), **les
coordonnées** (`CONTACT`) : même principe, on remplit la 4ᵉ valeur du tuple et
la pastille « à renseigner » disparaît.

**Le nom de domaine** (`DOMAINE`) sert aux balises canoniques. Les liens entre
pages sont relatifs : il n'y a rien d'autre à changer le jour où le domaine
est arrêté.

---

## Le formulaire B2B

Dans la démonstration statique l'envoi **n'est pas branché** : il n'y a ni
hébergement, ni adresse commerciale, ni CRM. Le formulaire valide bel et bien
tous les champs, puis affiche **exactement ce qui partirait**. Il ne dit pas
« envoyé ». Un accusé de réception sans destinataire est le pire des deux
mondes : le prospect croit qu'on l'a lu, et personne ne l'a lu.

Pour le brancher sur l'hébergement :

1. déposer `formulaire.php` à côté des pages ;
2. y renseigner `$DESTINATAIRE` (l'adresse commerciale AMARO) et
   `$EXPEDITEUR` (une adresse **du domaine** — mettre celle du prospect ferait
   échouer SPF et DKIM, et le courriel finirait en indésirable) ;
3. dans `page_amaro.py`, mettre `ACTION_FORMULAIRE = 'formulaire.php'` ;
4. relancer `python3 page_amaro.py`.

`formulaire.php` valide côté serveur (il ne fait pas confiance au navigateur),
n'accepte que les secteurs connus, porte un piège à robots invisible, et
**enregistre la demande avant d'essayer de notifier** : si le serveur de
courriel est en panne, la demande est déjà sauvée. Tant que `$DESTINATAIRE`
est vide, il enregistre quand même et affiche noir sur blanc que personne n'a
été prévenu.

Les demandes vont dans `donnees/demandes.sqlite`. **Protéger ce dossier** :
il contient des coordonnées professionnelles.

```apache
# donnees/.htaccess
<IfModule mod_authz_core.c>
	Require all denied
</IfModule>
<IfModule !mod_authz_core.c>
	Order allow,deny
	Deny from all
</IfModule>
```

---

## Ce qui reste ouvert

- **Le CMS.** Le cahier des charges en demande un (14). Aujourd'hui le contenu
  vit dans `contenu.py` : un seul fichier, texte, sans balise à écrire. C'est
  suffisant pour travailler et ça ne coûte rien à héberger. Un vrai CMS
  (WordPress, ou un CMS découplé) est un chantier à part, et il dépend de
  l'hébergement retenu.
- **Le pays d'exploitation.** Il commande le prestataire de paiement, la TVA,
  le transport, les mentions légales, la politique de cookies et la
  formulation des allégations. C'est pour ça qu'**aucun prix n'apparaît nulle
  part** sur le site : un prix dépend du pays, de la devise, de la TVA, du
  transport et du contrat de distribution.
- **Le nom de domaine.**
- **Les photographies produit**, le jour où la bouteille est soufflée.
- **La carte géographique** de la page Distribution. Elle est aujourd'hui un
  tableau par région, qui répond à la même question (« où est AMARO, où
  cherche-t-elle ») sans dépendre d'une bibliothèque de cartes ni d'un service
  de tuiles extérieur. Si une vraie carte est souhaitée, la structure de
  données est déjà la bonne.

---

## Fichiers

```
contenu.py         tout le texte, les saveurs, les formats, la palette
bouteille.py       le dessin SVG de la bouteille + le script du 360
style_amaro.py     la feuille de style
page_amaro.py      construit les 14 pages
chemins.py         où écrire les pages (demo/ en local, racine en production)
captures-amaro.py  les captures d'écran
tests-amaro.py     97 contrôles sur les pages rendues
formulaire.php     traitement serveur du formulaire B2B
demo/              le site généré — c'est ce dossier qu'on déploie
```

---

## Les contrôles

`tests-amaro.py` interroge **la page rendue**, pas le générateur. Lire le code
ne dit pas quelle règle CSS a gagné, ni si une image est cassée, ni si un
formulaire a vraiment refusé un champ vide.

- débordement horizontal, sur 14 pages × 2 largeurs ;
- images et références SVG, dans le viewport uniquement ;
- **contraste WCAG**, calculé sur les couleurs que le navigateur produit ;
- bascule FR→EN : aucun texte français ne doit rester visible ;
- **la géométrie du 360°**, contre la formule, sur 10 angles ;
- **les champs vides** : la page doit afficher exactement ce que `contenu.py`
  déclare, et aucun ne doit avoir été rempli par une valeur inventée ;
- le formulaire B2B, réellement soumis : vide, courriel invalide, puis valide ;
- les filtres du catalogue, et leur compteur ;
- **sans JavaScript** : aucune page ne se vide, le catalogue reste complet.
