from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_user_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()

    def create_user(self, user):
        user_ent = User(**user)
        self.session.add(user_ent)
        self.session.commit()
        return user_ent

    def get_all_users(self):
        return self.session.query(User).all()

    def update(self, user_d):
        user = self.get_one(user_d.get("id"))
        user.username = user_d.get("username")
        user.role = user_d.get("role")

        self.session.add(user)
        self.session.commit()
