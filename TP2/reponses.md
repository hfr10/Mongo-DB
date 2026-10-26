# Pourquoi MongoDB est adapté pour ce type d'application ?

- Une publication et ses commentaires/likes sont stockés dans un seul document : une seule lecture suffit pour afficher un post complet, sans jointure.
- Le schéma est flexible : on peut ajouter des champs (image, vidéo, tags...) à certaines publications sans modifier toute la base.
- Le format JSON/BSON correspond directement aux objets manipulés en Python (dictionnaires) et aux réponses d'une API.
- MongoDB se met facilement à l'échelle horizontalement (sharding), utile pour un réseau social avec beaucoup de données et d'écritures.

# Quels seraient les inconvénients d'utiliser une base SQL dans ce cas ?

- Il faudrait plusieurs tables (users, publications, commentaires, likes) et des jointures pour afficher une seule publication, ce qui alourdit les requêtes.
- Le schéma est rigide : chaque nouveau type de contenu demande une migration de la structure des tables.
- Avec un très gros volume de likes et de commentaires, les jointures deviennent coûteuses et la base est plus difficile à répartir sur plusieurs serveurs.
- Il faut convertir les lignes des tables en objets imbriqués côté application.
