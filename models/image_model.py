import os.path
import requests
import sys
import sqlite3 as sql
import datetime
import json
import socket
import hashlib
import os
import cherrypy
from models import object_model
from PIL import Image
import PIL, sys


# PROCESS OBJECTS IN IMAGE
def detect_objects(image):
    session = requests.Session()
    URL="http://image-dnn-sgh-jpbarraca.ws.atnog.av.it.pt/process"
    with open(image, 'rb') as f:
        file = {'img': f.read()}
        results = session.post(url=URL, files=file, data=dict(thr=0.2))
        image_obj = Image.open(image)
        if results.status_code == 200:
            i = 0
            for r in results.json():
                obj_path = 'croped_' + str(i) + '_' + str(os.path.basename(image))
                border = (r["box"]["x"], r["box"]["y"], r["box"]["x1"], r["box"]["y1"])
                cropped = image_obj.crop(border)
                cropped.save('resources/images/objs/' + obj_path, 'JPEG')
                object_model.insert_new_object(r, obj_path, md5_checksum(image), md5_checksum('resources/images/objs/' + obj_path))
                i += 1


def md5_checksum(file):
    h  = hashlib.md5()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(file, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


# IMAGES DATABASE OPERATIONS

def all_images():
    con = sql.connect("database.db")
    db = con.cursor()
    statement = "SELECT * from images"
    db.execute(str(statement))
    result = db.fetchall()
    db.close()
    return json.dumps(result)


def insert_new_image(image):
    con = sql.connect("database.db")
    db = con.cursor()
    statement = "INSERT INTO images (name, checksum, created_at) VALUES (?, ?,?)"
    data = (os.path.basename(image), md5_checksum(image), str(datetime.datetime.now().replace(microsecond=0)))
    db.execute(str(statement), data)
    con.commit()
    con.close()


def search_image_by_name(name):
    con = sql.connect("database.db")
    db = con.cursor()
    statement = "SELECT * from images WHERE name = ?"
    db.execute(str(statement), (name,))
    result = db.fetchone()
    db.close()
    return json.dumps(result)

def search_image_by_id(id):
    con = sql.connect("database.db")
    db = con.cursor()
    statement = "SELECT * from images WHERE checksum = ?"
    db.execute(str(statement), (id,))
    result = db.fetchone()
    db.close()
    json_result = []
    if not result:
        return 0
    else:
        json_result.append(
            {
                "id"     : result[0],  
                "name"  : result[1],
                "checksum"   : result[2],
                "created_at"  : result[3],
            }
        )
    return json.dumps(json_result)