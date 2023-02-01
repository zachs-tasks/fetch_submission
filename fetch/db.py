

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from typing import List
from user_login import UserLogin

class ServiceSessionManager:
    def __init__(self):
        self.engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/", echo=True)
        return


    def save_users(self, users: List[UserLogin]):
        with Session(self.engine) as session:
            session.add_all(users)
            session.commit()
        return