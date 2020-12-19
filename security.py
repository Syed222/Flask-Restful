"""
Authenticating user
"""
from Models.user import UserModel

# Creating user data using in memory data structure
# users = [
#     User(1, 'bob', 'asdf'),
#     User(2, 'jack', 'defg')
# ]
#
# user_mapping = {u.username: u for u in users}
# userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    """
    authenticates the user by using username and password
    """
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user


def security(payload):
    """
    Parses the payload data for the user Identity
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)


