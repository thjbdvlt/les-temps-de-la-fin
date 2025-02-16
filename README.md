# Les temps verbaux de _La fin du monde_ (Camille Flammarion)

Ce dépôt contient une version encodée en XML-TEI de _La fin du monde_, un roman scientifique de l'astronome Camille Flammarion.

## Contenu du dépôt

- [les-temps-de-la-fin.tei](les-temps-de-la-fin.tei): une version électronique du texte de _La fin du monde_, sans les paratextes mais avec les annotations morphologiques de tous les mots du texte, au format XML et accordement aux _guidelines_ TEI (avec quelques modifications, décrites dans le teiHeader). La documentation complète des enjeux, choix et méthodes d'encodage se trouve dans le _teiHeader_.
- plusieurs schémas permettant de valider ce fichier:
    - [tei-ud.odd](./tei-ud.odd): un [ODD](https://tei-c.org/guidelines/customization/getting-started-with-p5-odds/).
    - [tei-ud.dtd](./tei-ud.dtd) un DTD (une conversion de l'ODD par [Roma](https://roma.tei-c.org/)) qui exprime les mêmes règles que l'ODD et permet de valider le fichier contre la TEI à l'aide d'outil en ligne de commande comme `jing` ou `xmlstarlet` (voir le `makefile`).
    - un fichier Relax NG compact, bien plus strict que l'ODD et le DTD, et destiné surtout à exprimer la structure (très simple) du fichier.
- des scripts Python permettant de produire d'autres fichiers:
    - [to_html.py](to_html.py) permet de produire des fichiers HTML qui propose une colorisation des verbes en fonction des temps et modes verbaux, ainsi que des espèces d'_indices_ ou de tables des matières qui représentent le texte à partir des temps verbaux et permet (en cliquant sur les SVG), d'aller lire directement tel ou tel passage où, par exemple, l'usage du futur (rouge) est particulièrement dense.
    - [ud_to_msd.py](ud_to_msd.py) déplace les propriétés morphologiques (exprimées dans le fichier principal dans des attributs additionnels) dans l'attribut `@msd`.
- un `makefile` qui regroupe les différentes commandes:
    - `navigate`: ouvre dans le `$BROWSER` le fichier HTML principal.
    - `validate`: valide les fichiers contre les fichiers `.dtd` et `.rnc`.
    - `to_msd`: déplace les propriétés morphologiques vers l'attribut `@msd` et produit le fichier `les-temps-de-la-fin-no-ud.tei`.

## fichiers HTML

Pour consulter l'édition numérique du livre au format HTML, il suffit d'ouvrir le fichier `les-temps-de-la-fin.html` dans un navigateur[^1]. Les images ci-dessous montrent ce à quoi devrait ressembler la consultation. Les visualisations sont destinées à être utilisées pour effectuer une lecture tabulaire, par exemple pour aller consulter les passages où le conditionnel est très fréquent.

![](./img/haut.png)


![](./img/milieu.png)


![](./img/fut.png)

[^1]:  Les fichiers ont été testés sur Linux (Debian 12) avec Firefox.
