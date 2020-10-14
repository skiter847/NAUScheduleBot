from model import User


def user_exist(user_id):
    return User.select().where(User.id == user_id).exists()


def get_user_model(user_id):
    return User.select().where(User.id == user_id).get()


def get_user_ids():
    return [user_id for user_id in User.select().where(User.subscribe == True)]


