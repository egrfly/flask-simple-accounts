import bcrypt
from database.connection import get_db_connection


def add_user(name, email, password):
    with get_db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            password_bytes = password.encode()
            hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
            cursor.execute("""INSERT
                                INTO users
                                     (name, email, hashed_password)
                              VALUES (%s, %s, %s)""", [name, email, hashed_password])
            connection.commit()


def get_user_by_id(user_id):
    with get_db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("""SELECT u.id, u.name, u.email
                                FROM users AS u
                               WHERE u.id = %s""", [user_id])
            user = cursor.fetchone()
            return user


def get_user_with_credentials(email, password):
    with get_db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            password_bytes = password.encode()
            cursor.execute("""SELECT u.id, u.name, u.email, u.hashed_password
                                FROM users AS u
                               WHERE u.email = %s""", [email])
            user = cursor.fetchone()
            if user and bcrypt.checkpw(password_bytes, user.get('hashed_password')):
                return user


def email_available(email):
    with get_db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("""SELECT u.id, u.name, u.email
                                FROM users AS u
                               WHERE u.email = %s""", [email])
            user = cursor.fetchone()
            return True if user is None else False
