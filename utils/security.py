from werkzeug.security import generate_password_hash,check_password_hash

def hash_password(password):
   return generate_password_hash(password)

def verify_password(hashed_password,plain_password):
    return check_password_hash(hashed_password,plain_password)

def hash_otp(otp):
    return generate_password_hash(str(otp))

def verify_otp(hashed_otp,plain_otp):
    return check_password_hash(hashed_otp,plain_otp)           