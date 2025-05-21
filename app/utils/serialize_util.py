def serialize_object_to_dict(obj: dict):
    new_dict = {}
    if hasattr(obj, '__dict__'):
        for key, value in obj:
            new_dict[key]= value
    return new_dict