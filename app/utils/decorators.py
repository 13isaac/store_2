from functools import wraps
from flask_jwt_extended import verify_jwt_in_request,get_jwt_identity
from flask import jsonify
import json

def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args,**kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args,**kwargs)
        except Exception as e:
            return jsonify({"error":str(e)})
    return wrapper

def role_required(roles=[]):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args,**kwargs):
            try:
                verify_jwt_in_request()
                current_user=get_jwt_identity()
                roles_user=json.loads(current_user.get("roles",[]))
                if not set(roles).intersection(roles_user):
                    return jsonify({"error":"Servicio no disponible para este rol"}), 403
                return fn(*args,**kwargs)
            except Exception as e:
                return jsonify({"error":str(e)}),403
        return wrapper
    return decorator