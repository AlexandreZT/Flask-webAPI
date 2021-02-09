from flask import Flask, jsonify, request
import os
from os import system, path
import sqlite3
# from sqlite3 import Error

app = Flask(__name__)

@app.route("/", methods=['GET']) # http://127.0.0.1:5000/
def index():    
    return jsonify("Monk AI", 200)

@app.route("/upload-photo", methods=['POST']) # example : "POST /upload_photo?name=garden&url=garden.png HTTP/1.1" # OK
def upload_photo():
    """
    Ajouter dans la base de données une photo
    Avec vérification qu'il n'y ait pas deux images avec le même nom
    """
    conn = sqlite3.connect('db.sqlite3')
    curs = conn.cursor()
    if request.method == "POST":
        name = request.args.get("name")
        url = request.args.get("url")
        query_check_if_exist = curs.execute("SELECT name FROM images WHERE name ='"+name+"'")
        if query_check_if_exist.fetchall() != []:
            return "Vous ne pouvez pas enregister l'image sous ce nom car celui-ci est déjà utilisé !"
        
        curs.execute("INSERT INTO images(name, url) VALUES('"+name+"','"+url+"')")
        conn.commit() # sauvegarde de la transaction
        return "L'image a bien été enregistré !"            

@app.route("/list-photos", methods=['GET']) # "example : GET /list-photos HTTP/1.1" # OK
def list_photos():
    """
    Afficher toutes les photos
    """
    conn = sqlite3.connect('db.sqlite3')
    curs = conn.cursor()
    if request.method == "GET":
        select = curs.execute("""SELECT * FROM images""")    
        return jsonify(select.fetchall())

@app.route("/create-tag", methods=['POST']) # example : "POST /create-tag?name=cat HTTP/1.1" # OK
def create_tag():
    """
    Ajouter un tag dans la base de données
    """
    conn = sqlite3.connect('db.sqlite3')
    curs = conn.cursor()

    if request.method == "POST":
        name = request.args.get("name")
        query = curs.execute("SELECT name FROM tags WHERE name='"+name+"'")
        if query.fetchall() != []:
            return "Le tag '"+name+"' existe déjà"   
                        
        curs.execute("INSERT INTO tags(name) VALUES('"+name+"')")
        conn.commit() # sauvegarde de la transaction
        return jsonify("Le tag '"+name+"' a bien été enregistré !")   

@app.route("/list-tags", methods=['GET']) # example : "GET /list-tags HTTP/1.1" # OK
def list_tags():
    """
    Afficher tous les tags disponible dans la base de données
    """
    conn = sqlite3.connect('db.sqlite3')
    curs = conn.cursor()
    if request.method == "GET":
        query = curs.execute("""SELECT name FROM tags""")    
        return jsonify(query.fetchall())

@app.route("/add-image-tag", methods=['POST']) # example : "POST /add-image-tag?tag-name=dog&image-name=photo HTTP/1.1" # OK
def add_image_tag():
    """
    Ajoute un tag à une image # OK
    Si le tag existe alors oui on peut lui attribuer à une image si elle existe également # OK
    Mais seulement si l'image n'a pas déjà le tag 
    """
    conn = sqlite3.connect('db.sqlite3')
    curs = conn.cursor()
    if request.method == "POST":        
        tag_name = request.args.get("tag-name")
        image_name = request.args.get("image-name")

        query_get_image_id = curs.execute("SELECT id FROM images WHERE name='"+image_name+"'").fetchall() # image_exist ?
        query_get_tag_id = curs.execute("SELECT id FROM tags WHERE name='"+tag_name+"'").fetchall() # tag exist ?
    
        if query_get_tag_id != [] and query_get_image_id != []: # OK 
            image_id = query_get_image_id[0][0]                 
            query_get_image_id_tags = curs.execute("SELECT tag_id FROM image_tags WHERE image_id='"+str(image_id)+"'").fetchall() # already have id ?

            if (query_get_tag_id[0] in query_get_image_id_tags):
                return "L'image possède déjà ce tag !" # OK
            else:
                tag_id = query_get_tag_id[0][0] 
                print(tag_id)
                curs.execute("INSERT INTO image_tags (tag_id, image_id) VALUES('"+str(tag_id)+"', '"+str(image_id)+"')")  
                conn.commit() # sauvegarde de la transaction
                return "Le tag a été ajouter à l'image !" # OK        
        else: 
            return "Le tag n'existe pas ou l'image n'existe pas !" # OK

@app.route("/list-image-tags/<name>", methods=['GET']) # example : "GET /list-image-tags/photo HTTP/1.1" # OK
def list_image_tags(name): # le nom de l'image
    """
    Affiche tous les tags d'une image
    Recup l'id de l'image dans la table image WHERE name = args.name # OK : image_id
    Chercher tous les tag_id dans la table image_tags WHERE image_id = image_id # OK : list_tag_id
    FOR tag_id in tags_id => SELECT les names dans la table tags WHERE id = tag_id # OK : list_tag_name
    """
    conn = sqlite3.connect('db.sqlite3')
    curs = conn.cursor()

    query_select_image_id = curs.execute("SELECT id FROM images WHERE name='"+name+"'").fetchall()

    if query_select_image_id == []:
        return "Cette image n'existe pas !"

    image_id = query_select_image_id[0][0] # OK

    query_all_tag_id = curs.execute("SELECT tag_id FROM image_tags WHERE image_id ='"+str(image_id)+"'").fetchall()

    if query_all_tag_id == []:
        return "Cette image ne possède aucun tag !"

    list_tag_id = []
    for tag_id in query_all_tag_id:
        list_tag_id+=tag_id

    list_tag_name = []
    for tag_id in list_tag_id:
        list_tag_name += curs.execute("SELECT name FROM tags WHERE id='"+str(tag_id)+"'").fetchall()     

    return jsonify(list_tag_name)

@app.route("/list-tagged-images/<name>", methods=['GET']) # example : "GET /list-tagged-images/dog HTTP/1.1" # OK
def list_tagged_images(name): # le nom d'un tag
    """
    Affiche toutes les images ayant un tag spécifique
    """
    conn = sqlite3.connect('db.sqlite3')
    curs = conn.cursor()
    if request.method == "GET":
        query_get_tag_name_id = curs.execute("SELECT id FROM tags WHERE name='"+name+"'").fetchall()
        if query_get_tag_name_id == []:
            return "Ce tag n'existe pas !"
            
        tag_name_id = query_get_tag_name_id[0][0]

        query_select_image_id = curs.execute("SELECT image_id FROM image_tags where tag_id='"+str(tag_name_id)+"'").fetchall() # toutes les images (iddes images) ayant le tag

        if query_select_image_id == []:
            return "Aucune image ne possède ce tag !"

        list_image_id = []
        for image_id in query_select_image_id:
            list_image_id+=image_id

        list_image_name = []
        for image_id in list_image_id:
            list_image_name += curs.execute("SELECT name from images where id='"+str(image_id)+"'").fetchall()

        return jsonify(list_image_name)
        
@app.route('/create-collection', methods=['POST']) # example : "POST /create-collection?name=fish HTTP/1.1" OK
def create_collection():
    """
    Je créer une collection d'images si celle-ci n'existe pas
    """
    conn = sqlite3.connect('db.sqlite3')
    curs = conn.cursor()
    if request.method == "POST":
        name = request.args.get("name")
        query_check_if_exist = curs.execute("SELECT name FROM collections WHERE name='"+name+"'")
        if query_check_if_exist.fetchall() != []:
            return "Ce nom est déjà prit !"
        
        curs.execute("INSERT INTO collections(name) VALUES('"+name+"')")
        conn.commit() # sauvegarde de la transaction
        return "La collection a bien été enregistré !" 

@app.route('/add-image-in-collection', methods=['POST'])
def add_image_in_collection():
    """
    # TODO Ajouter une image dans une collection,
    L'image doit exister, la collection également, # OK
    L'image ne doit pas être déjà présente dans la collection # OK
    """
    conn = sqlite3.connect('db.sqlite3')
    curs = conn.cursor()
    if request.method == "POST":
        image_name = request.args.get("image-name") # => chercher l'id de l'image
        collection_name = request.args.get("collection-name") # => chercher l'id de la collection

        image_id = curs.execute("SELECT id FROM images WHERE name='"+image_name+"'").fetchall()
        collection_id = curs.execute("SELECT id FROM collections WHERE name='"+collection_name+"'").fetchall()

        if image_id != [] and collection_id != []: # check if image and collection exists or not
            query_check_if_image_is_in_the_collection = curs.execute("SELECT image_id FROM images_collection WHERE image_id='"+str(image_id)+"'").fetchall()
            if query_check_if_image_is_in_the_collection == []:
                # return "L'image ne fait pas parti de la collection et pourra être ajouté !"
                query_add = curs.execute("INSERT INTO images_collection(image_id, collection_id) VALUES ('"+str(image_id)+"', '"+str(collection_id)+"') ")
                return "L'image a été ajouté dans la collection !"
            else:
                return "L'image est déjà présente dans la collection ! "
        else:
            return "L'image ou la collection n'existe pas !"

@app.route('/remove-image-from-collection', methods=['DELETE'])
def remove_image_from_collection():
    """
    Supprimer une image d'une collection
    """
    if request.method == "DELETE": # => DROP COLUMN
        pass

@app.route('/not_found', methods=['GET'])
def not_found():
    return jsonify(message='That resource was not found'), 404

def setup_database(): # OK
    """
    Connexion et setup de la base de données
    List des types : NULL, INTEGER, REAL, TEXT & BLOB.
    """
    # S'il n'y a pas de base de donnée, je créer le fichier sqlite
    if path.exists("db.sqlite3") == False:
        file = open("db.sqlite3", "w") 
        file.close()

    # Connection à la base de données sqlite (c'est un fichier)
    # conn = sqlite3.connect(os.getcwd()+'\\db.sqlite3') # alternative
    conn = sqlite3.connect('db.sqlite3')
    curs = conn.cursor() # curs me permet d'utiliser la bdd, curs.execute('requete SQL')

    # Création de la table images (id, nom, url, size, tags 1-n (aucun par défaut), collection 1-n (aucun par défaut))
    curs.execute("""CREATE TABLE IF NOT EXISTS images(
        id INTEGER PRIMARY KEY,
        name TEXT,
        url TEXT,
        width INTEGER,
        height INTEGER,
        type TEXT
        )"""
    )
    
    # Création de la table tags (id, name)
    curs.execute("""CREATE TABLE IF NOT EXISTS tags(
        id INTEGER PRIMARY KEY,
        name TEXT
        )"""
    )

    # Création de la table image-tags (id, name, id_image)
    curs.execute("""CREATE TABLE IF NOT EXISTS image_tags(
        id INTEGER PRIMARY KEY,
        tag_id INTEGER,
        image_id INTEGER,
        FOREIGN KEY(tag_id) REFERENCES tags(id),
        FOREIGN KEY(image_id) REFERENCES images(id)
        )"""
    )

    # Création de la table collections (id, name, collection d'images)
    curs.execute("""CREATE TABLE IF NOT EXISTS collections(
        id INTEGER PRIMARY KEY,
        name TEXT
        )"""
    )

    # Création de la table images_collection (id, name, collection d'images)
    curs.execute("""CREATE TABLE IF NOT EXISTS images_collection(
        id INTEGER PRIMARY KEY,
        collection_id INTEGER,
        image_id INTEGER,
        FOREIGN KEY(image_id) REFERENCES images(id),
        FOREIGN KEY(collection_id) REFERENCES collections(id)
        )"""
    )   

if __name__ == '__main__':
    setup_database() # Création des tables si nécessaire
    # http://127.0.0.1:5000
    debug=False
    app.run(debug)

"""
## Personal notes :

# Envoyer des requêtes HTTP avec : 
=> https://www.postman.com/

# Pour définir les méthodes autorisé pour une route : 
=> methods=["GET", "POST", "PUT", "DELETE"]

# Si on récup de la donnée au format json :
=> request.get_json()["name"]

# Si on récup de la donnée depuis un formulaire :
=> request.form.get("name") 

# Si on récup de la donnée depuis une reqûete :
=> request.args.get("name")
"""