import os.path
import os
import requests
import sys
import sqlite3 as sql
import datetime
import json
import socket
import hashlib
from models import image_model
from PIL import Image

def compute_average_image_color(img):
    width, height = img.size

    r_total = 0
    g_total = 0
    b_total = 0

    count = 0
    for x in range(0, width):
        for y in range(0, height):
            r, g, b = img.getpixel((x,y))
            r_total += r
            g_total += g
            b_total += b
            count += 1

    return (r_total/count, g_total/count, b_total/count)

# OBJECTS DATABASE OPERATIONS
def all_objects_name():
    con = sql.connect("database.db")
    db = con.cursor()
    statement = "SELECT id,class,confidence from objects ORDER BY id DESC"
    db.execute(str(statement))
    result = db.fetchall()
    json_result = []
    for obj in result:
        json_result.append(
            {
                "id"     : obj[0],  
                "class"  : obj[1],
                "confidence" : obj[2]
            }
        )
    return json.dumps(json_result)

def all_objects_detected():
    con = sql.connect("database.db")
    db = con.cursor()
    statement = "SELECT * from objects ORDER BY id DESC"
    db.execute(str(statement))
    result = db.fetchall()
    json_result = []
    for obj in result:
        json_result.append(
            {
                "id"     : obj[0],  
                "class"  : obj[1],
                "name"   : obj[2],
                "image"  : obj[3],
                "confidence" : obj[4],
                "original" : obj[5],
            }
        )
    return json.dumps(json_result)

def all_objects_detected_name(name):
    con = sql.connect("database.db")
    db = con.cursor()
    statement = "SELECT * from objects ORDER BY id DESC"
    db.execute(str(statement))
    result = db.fetchall()
    json_result = []
    for obj in result:
        if(obj[1].lower() == name.lower()):
            json_result.append(
                {
                    "id"     : obj[0],  
                    "class"  : obj[1],
                    "name"   : obj[2],
                    "image"  : obj[3],
                    "confidence" : obj[4],
                    "original" : obj[5],
                }
            )
    return json.dumps(json_result)

def all_objects_detected_name_color(name, color):
    con = sql.connect("database.db")
    db = con.cursor()
    statement = "SELECT * from objects ORDER BY id DESC"
    db.execute(str(statement))
    result = db.fetchall()
    json_result = []
    for obj in result:
        if(obj[1].lower() == name.lower()):
            obj_img = Image.open('resources/images/objs/' + obj[2])
            avarage_colors = compute_average_image_color(obj_img)
            dominant_color_value = max(avarage_colors)

            for i in range (0, len(avarage_colors)):
                if dominant_color_value == avarage_colors[i]:
                    if i == 0:
                        dominant_color_name = 'red'
                    elif i == 1:
                        dominant_color_name = 'green'
                    else:
                        dominant_color_name = 'blue'
                        
            if color.lower() == dominant_color_name:
                json_result.append(
                    {
                        "id"     : obj[0],  
                        "class"  : obj[1],
                        "name"   : obj[2],
                        "image"  : obj[3],
                        "confidence" : obj[4],
                        "original" : obj[5],
                    }
                )
    return json.dumps(json_result)


def search_objects_by_image_id(image_id):
    con = sql.connect("database.db")
    db = con.cursor()
    statement = "SELECT * from objects WHERE image_id = ?"
    db.execute(str(statement), (image_id,))
    result = db.fetchall()
    db.close()
    return json.dumps(result)

def search_objects_by_id(id):
    con = sql.connect("database.db")
    db = con.cursor()
    statement = "SELECT * from objects WHERE image = ?"
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
                "class"  : result[1],
                "name"   : result[2],
                "image"  : result[3],
                "confidence" : result[4],
                "original" : result[5],
            }
        )
    return json.dumps(json_result)

def search_objects_by_name(name):
    con = sql.connect("database.db")
    db = con.cursor()
    statement = "SELECT * from objects WHERE class = ?"
    db.execute(str(statement), (name,))
    result = db.fetchall()
    db.close()
    return json.dumps(result)

def insert_new_object(obj, path, original, image):
    con = sql.connect("database.db")
    db = con.cursor()
    statement = "INSERT INTO objects (class, name, image, confidence, original, created_at) VALUES (?, ?, ?, ?, ?, ?)"
    curDateTime = datetime.datetime.now().replace(microsecond=0)
    data = (str(obj["class"]), str(path), str(image), str(round(obj['confidence'] * 100)) ,str(original), str(curDateTime))
    db.execute(str(statement), data)
    con.commit()
    con.close()

def delete_object(id):
    con = sql.connect("database.db")
    db = con.cursor()
    '''statement = "SELECT image,original FROM objects WHERE id = ?"
    db.execute(str(statement), (id,))
    file_name = db.fetchall()
    
    statement = "SELECT name FROM objects WHERE original = ?"
    db.execute(str(statement), (file_name[1],))
    count = len(db.fetchall())
    
    if count == 1:
        delete_file("original/" + file_name[1])
    
    delete_file("objs/" + file_name[0])'''
    

    statement = "DELETE FROM objects WHERE id = ?"
    db.execute(str(statement), (id,))
    con.commit()
    con.close()
    

def delete_file(file_name):
    os.remove("/resources/images/" + file_name)

def delete_all():
    con = sql.connect("database.db")
    db = con.cursor()

    statement = "DELETE FROM objects"
    db.execute(str(statement))
    
    con.commit()
    con.close()
    return 'success'

def edit(id, obj, confidence): #obj -> class
    con = sql.connect("database.db")
    db = con.cursor()
    statement = "UPDATE objects SET class = ?, confidence = ? WHERE image = ?"
    db.execute(str(statement), (str(obj), str(confidence), str(id)),)
    con.commit()
    con.close()
    return 'success'