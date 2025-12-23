from app.repositories.user_repo import UserRepository
from app.models.user import User
from passlib.hash import bcrypt

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, email: str, password: str, role: str = "user"):
        hashed_password = bcrypt.hash(password)
        user = User(email=email, hashed_password=hashed_password, role=role)
        return self.user_repo.create(user)

    def get_user(self, user_id):
        return self.user_repo.get_by_id(user_id)

    def get_by_email(self, email: str):
        return self.user_repo.get_by_email(email)

    def list_users(self):
        return self.user_repo.list_all()
