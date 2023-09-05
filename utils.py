from bson import json_util, ObjectId
import json
from datetime import datetime
from bson.decimal128 import Decimal128

def serialize_mongo_object(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, Decimal128):
        return float(obj.to_decimal())
    raise TypeError(f"Object type {type(obj).__name__} not serializable")

def mongo_to_json(data):
    return json.loads(json_util.dumps(data))