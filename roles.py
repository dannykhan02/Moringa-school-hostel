# from flask import jsonify
# from flask_jwt_extended import get_jwt_identity, jwt_required
# from functools import wraps

# def role_required(required_role):
#     def decorator(fn):
#         @wraps(fn)
#         @jwt_required()
#         def wrapper(*args, **kwargs):
#             current_user = get_jwt_identity()
#             if 'role' not in current_user:
#                 return jsonify({'message': 'Role not found in token'}), 403

#             if current_user['role'] != required_role:
#                 return jsonify({'message': 'Access forbidden: Insufficient role'}), 403

#             return fn(*args, **kwargs)
#         return wrapper
#     return decorator
