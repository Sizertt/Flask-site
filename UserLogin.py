from scripts.db import DB

from flask_login import UserMixin


class UserLogin(UserMixin):
    def fromDB(self, user_id):
        self.__user = DB().getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        print(self.__user)
        return str(self.__user[0][0])
