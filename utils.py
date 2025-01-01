import bcrypt

def hash_password(password):
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed 