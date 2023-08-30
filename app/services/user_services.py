# services.py

from ..repos.user_repos import UserRepository

# TODO: Create, Update, Delete


class UserService():
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    # Retrieve
    def retrieve_all_users(self):
        return self.repository._retrieve_all_users()

    def get_by_username(self, username: str):
        if username != "test":
            return None
        else:
            return True
