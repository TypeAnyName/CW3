import base64
import hashlib
import hmac

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from project.dao.users import UserDAO


class UserService:
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    def get_one(self, uid):
        return self.user_dao.get_one(uid)

    def get_all(self):
        return self.user_dao.get_all()

    def update(self, uid):
        self.user_dao.update(uid)
        return self.user_dao

    def get_user_by_email(self, email):
        return self.user_dao.get_user_by_email(email)

    def generate_user_password(self, password):
        hash_digest = self.get_hash(password)
        return base64.b64encode(hash_digest)

    def get_hash(self, password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

    def create(self, user):
        user['password'] = self.generate_user_password(user["password"])
        return self.user_dao.create_user(user)

    def compare_passwords(self, password_hash, other_password):
        return hmac.compare_digest(
            base64.b64decode(password_hash),
            hashlib.pbkdf2_hmac(
                'sha256',
                other_password.encode('utf-8'),
                PWD_HASH_SALT,
                PWD_HASH_ITERATIONS
            )
        )

    def update_part(self, data, uid):
        user = self.user_dao.get_one(uid)

        if 'name' in data:
            user.name = data['name']
        if "surname" in data:
            user.surname = data["surname"]
        if "favorite_genre" in data:
            user.favorite_genre = data["favorite_genre"]

        self.user_dao.update(user)

