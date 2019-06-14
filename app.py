#!python
# Example of a cherrypy application that serves static content,
# as well as dynamic content.
#
# JMR@ua.pt 2016
#
# To run:
#	python exampleApp.py

import os.path
import cherrypy
import json
from models import object_model
from models import image_model

# The absolute path to this file's base directory:
baseDir = os.path.dirname(os.path.abspath(__file__))

# Dict with the this app's configuration:
config = {
  "/":     { "tools.staticdir.root": baseDir },
  "/js":   { "tools.staticdir.on": True,
             "tools.staticdir.dir": "resources/js" },
  "/css":  { "tools.staticdir.on": True,
             "tools.staticdir.dir": "resources/css" },
  "/html": { "tools.staticdir.on": True,
             "tools.staticdir.dir": "resources/html" },
  "/fonts": { "tools.staticdir.on": True,
            "tools.staticdir.dir": "resources/fonts" },
  "/bootstrap": { "tools.staticdir.on": True,
             "tools.staticdir.dir": "resources/bootstrap" },
  "/images": { "tools.staticdir.on": True,
             "tools.staticdir.dir": "resources/images" },
  "/icons": { "tools.staticdir.on": True,
             "tools.staticdir.dir": "resources/icons" },
}

class Root:
  # This class atribute contains the HTML text of the main page:
  indexHTML = open('resources/html/index.html', 'r').read()
  searchByNameHTML = open('resources/html/searchbyname.html', 'r').read()
  newImageHTML = open('resources/html/newimage.html', 'r').read()
  searchByNameAndColorHTML = open('resources/html/searchbynameandcolor.html', 'r').read()
  aboutHTML = open('resources/html/about.html','r').read();
  editHTML = open('resources/html/edit.html','r').read();

  @cherrypy.expose
  def index(self):
      return Root.indexHTML
  
  @cherrypy.expose
  def search_by_name(self):
    return Root.searchByNameHTML
  
  @cherrypy.expose
  def search_by_name_and_color(self):
    return Root.searchByNameAndColorHTML

  @cherrypy.expose
  def sendImages(self):
    return Root.newImageHTML

  @cherrypy.expose
  def about(self):
    return Root.aboutHTML

  @cherrypy.expose
  def edit(self, **params):
    return Root.editHTML

  @cherrypy.expose
  def list(self, type, name="all", color="all"):
    if type == "names":
      return object_model.all_objects_name()
    elif type == "detected":
      if name == "all":
        if color == "all":
          return object_model.all_objects_detected()
      else:
        if color == "all":
          return object_model.all_objects_detected_name(name)
        else:
          return object_model.all_objects_detected_name_color(name, color)

  @cherrypy.expose
  def get(self, id):
    result = object_model.search_objects_by_id(id)
    if result == 0:
      result = image_model.search_image_by_id(id)
      if result == 0:
        return json.dumps("not found")
    return result
  @cherrypy.expose
  def put(self, image):
    saved_img_location = os.getcwd()+ '/resources/images/original/' + image.filename
    fo = open(saved_img_location, 'wb')
    while True:
      data = image.file.read(8192)
      if not data:
        break
      fo.write(data)
    fo.close()
    image_model.insert_new_image(saved_img_location)
    image_model.detect_objects(saved_img_location)
    return 'success'

  @cherrypy.expose
  def delete_object(self, id):
    if id == "all":
      count = len(json.loads(object_model.all_objects_detected()))
      if count == 0: return json.dumps("Database already empty")
      else : 
        object_model.delete_all()
        return json.dumps("success")
      
    else:
      object_model.delete_object(id)
      return json.dumps("success")

  @cherrypy.expose
  def edit_object(self, id, obj, confidence):
      object_model.edit(id, obj, confidence)
      return json.dumps("Object updated")
  
cherrypy.config.update({'server.host' : '127.0.0.1'}) 
cherrypy.config.update({'server.socket_port' : 8080})
cherrypy.quickstart(Root(), "/", config)