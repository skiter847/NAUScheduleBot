from model import User


def user_exist(user_id):
    return User.select().where(User.id == user_id).exists()


def get_user_model(user_id):
    return User.select().where(User.id == user_id).get()
