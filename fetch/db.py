from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from typing import List
from user_login import UserLogin

"""
Hopefully self-documenting
"""
class ServiceSessionManager:

    # wouldn't have the default for production code
    def __init__(self, connection_string: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/"):
        self.engine = create_engine(connection_string)
        return

    def save_users(self, users: List[UserLogin]):
        with Session(self.engine) as session:
            session.add_all(users)
            session.commit()
        return

    def get_users(self, user_ids: List[str]) -> List[UserLogin]:
        with Session(self.engine) as session:
            users = session.query(UserLogin).filter(UserLogin.user_id.in_(user_ids)).all()
        return users


    def select_all(self) -> List[UserLogin]:
        with Session(self.engine) as session:
            data = session.query(UserLogin).all()
        return data
