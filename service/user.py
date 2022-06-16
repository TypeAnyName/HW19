import base64
import hashlib
import hmac

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all_users()

    def update(self, user_d):
        self.dao.update(user_d)
        return self.dao

    def get_user_by_username(self, username):
        return self.dao.get_user_by_username(username)

    def generate_user_password(self,password):
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
        return self.dao.create_user(user)

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
