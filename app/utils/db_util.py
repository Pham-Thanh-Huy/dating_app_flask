from app import db

def delete_list(object_list):
    for obj in object_list:
        db.session.delete(obj)
