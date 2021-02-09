# Monk API
Pour lancer le programme vous devez disposez de python : https://www.python.org/downloads/
et du package flask : pip install flask.

Afin de lancer le programme vous devez simplement lancer le programme main.py.
La base de donnée fonctionne avec sqlite,
Si vous souhaitez réinitialiser la base de données, vous n'avez qu'à supprimer le fichier db.sqlite3 et relancer le programme.
Le programme se chargera de recréer le fichier et de créer les tables de la base de données en local si nécessaire.

Pour tester cette api vous pouvez vous rendre sur https://www.postman.com/ afin d'installer postman Desktop agent

Une fois ce logiciel lancer, vous pouvez retourner sur le site https://www.postman.com/ afin d'effectuer vos requêtes

La listes des reqûetes disponibles sont les suivantes : 

http://127.0.0.1:5000//upload-photo # example : "POST /upload_photo?name=garden&url=garden.png HTTP/1.1"

http://127.0.0.1:5000//list-photos # example : "GET /list-photos HTTP/1.1"

http://127.0.0.1:5000//create-tag # example : "POST /create-tag?name=cat HTTP/1.1"

http://127.0.0.1:5000//list-tags # example : "GET /list-tags HTTP/1.1"

http://127.0.0.1:5000//add-image-tag # example : "POST /add-image-tag?tag-name=dog&image-name=photo HTTP/1.1"

http://127.0.0.1:5000//list-image-tags/<name> # example : "GET /list-image-tags/photo HTTP/1.1"

http://127.0.0.1:5000//list-tagged-images/<name> # example : "GET /list-tagged-images/dog HTTP/1.1"

Autres reqûetes de collections disponibles :

http://127.0.0.1:5000//create-collection # example : "POST /create-collection?name=fish HTTP/1.1"

http://127.0.0.1:5000//add-image-in-collection # en développement : "POST /add-image-in-collection?image-name=photo&collection-name=fish HTTP/1.1"

http://127.0.0.1:5000//remove-image-from-collection # en développement : "DELETE /remove-image-from-collection?image-name=photo&collection-name=fish HTTP/1.1"