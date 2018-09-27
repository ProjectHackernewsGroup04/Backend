import bcrypt
import database

# Global variables
db_con = database.get_db_conn()


def prepare():
    database.prepare_db()
    print("ASDASD")


def check_login_success(username, password):
    users = db_con.users
    login_user = users.find_one({'username': username})
    print('Trying loggin', username)
    if login_user:
        stored_password = login_user['password']
        # Comparing stored password and the users hashed password
        if bcrypt.hashpw(password.encode('utf8'),
                         stored_password) == stored_password:
            print('Login Success')
            return True
        else:
            print('Login Failed bad password')
            return False
    print('Login Failed user dont exist')
    return False


def check_register_success(username, password):
    try:
        print("asda")
        print('Trying registering', username)
        users = db_con.users
        existing_user = users.find_one({'username': username})
        print('Trying registering', username)
        if existing_user is None:
            hashed = bcrypt.hashpw(password.encode('utf8'),
                                   bcrypt.gensalt())  # Hashed pw
            print(hashed)
            users.insert(
                {'username': username, 'password': hashed})
            return True
        else:
            print('Register Failed')
            return False
    except Exception as e:
        print(str(e))
