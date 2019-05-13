import os.path
import cherrypy
import requests
import sys
import sqlite3 as sql
import datetime
import json
import socket


# The absolute path to this file's base directory:
baseDir = os.path.dirname(os.path.abspath(__file__))

# Dict with the this app's configuration:
config = {
  "/":     { "tools.staticdir.root": baseDir },
  "/js":   { "tools.staticdir.on": True,
             "tools.staticdir.dir": "js" },
  "/css":  { "tools.staticdir.on": True,
             "tools.staticdir.dir": "css" },
  "/bootstrap":  { "tools.staticdir.on": True,
             "tools.staticdir.dir": "bootstrap" },
  "/fonts":  { "tools.staticdir.on": True,
             "tools.staticdir.dir": "fonts" },
  "/html": { "tools.staticdir.on": True,
             "tools.staticdir.dir": "html" },
}

class Root:
    
    # PROCESS OBJECTS IN IMAGE
    @cherrypy.expose
    def detect_objects(self, image_name):
        session = requests.Session()
        URL="http://image-dnn-sgh-jpbarraca.ws.atnog.av.it.pt/process"
        image_name = 'images/' + image_name
        with open(image_name, 'rb') as f:
            file = {'img': f.read()}
            r = session.post(url=URL, files=file, data=dict(thr=0.5))
            if r.status_code == 200:
                #print(r.json())
                self.insert_new_image(image_name)
                self.insert_new_object(r.json())

    # IMAGES DATABASE OPERATIONS
    @cherrypy.expose
    def all_images(self):
        con = sql.connect("database.db")
        db = con.cursor()
        statement = "SELECT * from images"
        db.execute(str(statement))
        result = db.fetchall()
        db.close()
        return json.dumps(result)

    @cherrypy.expose
    def insert_new_image(self, image_name):
        con = sql.connect("database.db")
        db = con.cursor()
        statement = "INSERT INTO images (name, created_at) VALUES (?, ?)"
        data = (str(image_name), str(datetime.datetime.now().replace(microsecond=0)))
        db.execute(str(statement), data)
        con.commit()
        con.close()

    @cherrypy.expose
    def search_image_by_name(self, name):
        con = sql.connect("database.db")
        db = con.cursor()
        statement = "SELECT * from images WHERE name = ?"
        db.execute(str(statement), (name,))
        result = db.fetchone()
        db.close()
        return json.dumps(result)

    @cherrypy.expose
    def image_count(self):
        con = sql.connect("database.db")
        db = con.cursor()
        statement = "SELECT * from images"
        db.execute(statement)
        result = len(db.fetchall())
        return json.dumps({"count" : result})
        

        

    # OBJECTS DATABASE OPERATIONS
    @cherrypy.expose
    def all_objects(self):
        con = sql.connect("database.db")
        db = con.cursor()
        statement = "SELECT * from objects"
        db.execute(str(statement))
        result = db.fetchall()
        db.close()
        return json.dumps(result)


    @cherrypy.expose
    def search_objects_by_image_id(self, image_id):
        con = sql.connect("database.db")
        db = con.cursor()
        statement = "SELECT * from objects WHERE image_id = ?"
        db.execute(str(statement), (image_id,))
        result = db.fetchall()
        db.close()
        return json.dumps(result)

    @cherrypy.expose
    def search_objects_by_name(self, name):
        con = sql.connect("database.db")
        db = con.cursor()
        statement = "SELECT * from objects WHERE type = ?"
        db.execute(str(statement), (name,))
        result = db.fetchall()
        db.close()
        return json.dumps(result)

    @cherrypy.expose
    def insert_new_object(self, object):
        con = sql.connect("database.db")
        db = con.cursor()
        statement = "INSERT INTO objects (type, image_id, created_at) VALUES (?, ?, ?)"
        data = (str(object[0].get('class')), str(self.search_image_by_name(object)[0]), str(datetime.datetime.now().replace(microsecond=0)))
        db.execute(str(statement), data)
        con.commit()
        con.close()


    @cherrypy.expose
    def object_count(self):
        con = sql.connect("database.db")
        db = con.cursor()
        statement = "SELECT * from objects"
        db.execute(statement)
        result = len(db.fetchall())
        return json.dumps({"count" : result})


    #@cherrypy.expose
    #def 



    # This class atribute contains the HTML text of the main page:
    indexPage = open(baseDir + '/html/index.html', 'r').read()
    
    #objects=Actions.all_objects(Actions)
    searchTypePage = open(baseDir + '/html/searchbytype.html', 'r').read()
    #searchTypeColorPage = open(baseDir + '/html/searchByType&Color.html', 'r').readlines()
    #sendImgPage = open(baseDir + '/html/sendImage.html', 'r').readlines()
    #objectsListedPage = open(baseDir + '/html/objects.html', 'r').readlines()
    #aboutPage = open(baseDir + '/html/about.html', 'r').readlines()

    
    
    @cherrypy.expose
    def index(self):
       return Root.indexPage

    @cherrypy.expose
    def api_test(self):
        return Root.all_objects(self)
    
    @cherrypy.expose
    def indedx(self):
        return Root.searchTypePage


'''
    @cherrypy.expose
    def searchType(self):
        return Root.searchTypePage

    @cherrypy.expose
    def searchTypeColor(self):
        return Root.searchTypeColorPage
    
    @cherrypy.expose
    def sendImage(self):
        return Root.sendImgPage
    
    @cherrypy.expose
    def objectsListed(self):
        return Root.objectsListedPage
      
    @cherrypy.expose
    def about(self):
        return Root.aboutPage
   '''

if __name__ == '__main__':
    cherrypy.server.socket_port = 8088
    cherrypy.quickstart(Root(), "/", config)






