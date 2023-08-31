from bson import json_util, ObjectId
import json

def serialize_mongo_object(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError("Object type not serializable")

def mongo_to_json(data):
    return json.loads(json_util.dumps(data))