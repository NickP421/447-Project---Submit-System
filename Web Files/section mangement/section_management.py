import pymongo
import base64
import bson
import os
from bson.binary import Binary
from db_func import *
#####################
###Constants
#####################

#####################

################
##Example of section document in collection:
##{"section" : 5,
##"students" : [{"ID": "12345", "name" : "Queen Victoria",
##"submissions" : [{"filename": "hw1.py", "file": "0110100001", "timestamp": "2008-05-03 15:23:16+00:00"}]}]
##"assignments": [{"filename" : "monopoly.py", "file": "010001010", "due date": "2020-01-01 00:00:00+00:00"}]}
##section dict contains student and assignments list of dicts; student dict contains submissions dicts
##coll_name represents which class the sections/students/etc are in
################

def add_section(sec_num, coll_name):
    client = connect_client()
    if client == -1:
        return -1
    
    db = connect_db(client)

    collection = connect_collection(db, coll_name)

    for doc in collection.find({}):
        if doc["section"] == sec_num:
            print("Section number already used")
            return -1
        
    collection.insert_one({"section": sec_num,
                           "students" : [],
                           "assignments" : []})
    return 0

def add_assignment(section, filepath, due_date, coll_name):
    client = connect_client()
    if client == -1:
        return -1
    
    db = connect_db(client)

    collection = connect_collection(db, coll_name)

    #iterate over documents in collection of sections    
    for doc in collection.find({}):
        if doc["section"] == section: #find correct section
            with open(filepath, 'rb') as f:
                encoded = Binary(f.read())
            f.close()
            filename = os.path.basename(filepath)
            assign_dict = {"filename" : filename,
                           "file" : encoded,
                           "due date": due_date}

            new_doc = doc
            new_doc["assignments"].append(assign_dict)

            #first parameter is for identifying which doc to update
            #second parameter is new document
            #upsert parameter will insert if doc is not found in def
            collection.update_one({"section": section}, {"$set" : new_doc}, upsert=False)
            return 0
                          
                
             
    #section not found
    print("Section not found")
    return -1



def remove_assignment(section, name, coll_name):
    client = connect_client()
    if client == -1:
        return -1
    
    db = connect_db(client)

    collection = connect_collection(db, coll_name)

    #iterate over documents in collection of sections    
    for doc in collection.find({}):
        if doc["section"] == section: #find correct section
            for i in range(len(doc["assignments"])):
                if doc["assignments"][i]["filename"] == name:

                    new_doc = doc
                    new_doc["assignments"].remove(new_doc["assignments"][i])

                    #first parameter is for identifying which doc to update
                    #second parameter is new document
                    #upsert parameter will insert if doc is not found in def
                    collection.update_one({"section": section}, {"$set" : new_doc}, upsert=False)
                    return 0
                          
                
             
    #section not found
    print("Section not found")
    return -1
    

#add student to section or overwrite student's name
def add_student(ID, name, section, coll_name):
    client = connect_client()
    if client == -1:
        return -1
    
    db = connect_db(client)

    collection = connect_collection(db, coll_name)

    #iterate over documents in collection of sections    
    for doc in collection.find({}):
        if doc["section"] == section: #find correct section
            #see if student is already in section
            for student_dict in doc["students"]:
                if student_dict["ID"] == ID:
                    print("student already exists in section")
                    return -1
            #student not found; create dict and append to list of student dicts
            student_dict = {"ID": ID, "name": name, "submissions": []}

            new_doc = doc
            new_doc["students"].append(student_dict)
            #first parameter is for identifying which doc to update
            #second parameter is new document
            #upsert parameter will insert if doc is not found in db
            collection.update_one({"section" : section}, {"$set" : new_doc}, upsert=False)
            return 0
    #section not found
    print("Section not found")
    return -1

#change student's name in student dictionary
def modify_student(ID, name, section, coll_name):
    client = connect_client()
    if client == -1:
        return -1
    
    db = connect_db(client)

    collection = connect_collection(db, coll_name)

    #iterate over documents in collection of sections    
    for doc in collection.find({}):
        if doc["section"] == section:
            #iterate over list of student dictionaries
            for i in range(len(doc["students"])):
                #if the ith student dict has a matching ID, we've found our student
                if doc["students"][i]["ID"] == ID:
                   #update student name
                    new_doc = doc
                    new_doc["students"][i]["name"] = name

                    #first parameter is for identifying which doc to update
                    #second parameter is new document
                    #upsert parameter will insert if doc is not found in def
                    collection.update_one({"section": section}, {"$set" : new_doc}, upsert=False)
                    return 0
                
            print("student ID not found")
            return -1
    print("section not found")
    return -1


def remove_student(ID, section, coll_name):
    client = connect_client()
    if client == -1:
        return -1
    
    db = connect_db(client)

    collection = connect_collection(db, coll_name)

    #iterate over documents in collection of sections    
    for doc in collection.find({}):
        if doc["section"] == section:
            #iterate over list of student dictionaries
            for i in range(len(doc["students"])):
                #if the ith student dict has a matching ID, we've found our student
                if doc["students"][i]["ID"] == ID:
                   #update student name
                    new_doc = doc
                    new_doc["students"].remove(new_doc["students"][i])

                    #first parameter is for identifying which doc to update
                    #second parameter is new document
                    #upsert parameter will insert if doc is not found in def
                    collection.update_one({"section": section}, {"$set" : new_doc}, upsert=False)
                    return 0
                
            print("student ID not found")
            return -1
    print("section not found")
    return -1

            
