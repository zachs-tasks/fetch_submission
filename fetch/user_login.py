from __future__ import annotations

from sqlalchemy import String, Date, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column, relationship
from datetime import datetime
from typing import Dict, List, Optional

"""
If this were production, I would use the AWS API boto3. There's a bit of credential configuration that would need to be added
to the production machine in order for this API to work.
"""
import data_mask
import json

class Base(DeclarativeBase):
    pass

class UserLogin(Base):
    __tablename__ = "user_logins"


    """
    These all shouldn't be primary keys. The postgres table didn't have a primary key.
    This is a quick & dirty workaround in order to use the ORM. I could just use plain old SQL.
    """
    user_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    device_type: Mapped[str] = mapped_column(String(32), primary_key=True)
    masked_ip: Mapped[str] = mapped_column(String(256), primary_key=True)
    masked_device_id: Mapped[str] = mapped_column(String(256), primary_key=True)
    locale: Mapped[str] = mapped_column(String(32))

    """
    If I had more time, I would maybe add a new "Versions Table"
    which maps ints to the string version numbers
    """
    app_version: Mapped[int] = mapped_column(Integer)

    create_date: Mapped[datetime] = mapped_column(Date)


    # for validation purposes
    KEYS: Dict[None] = {
                        "user_id": None, 
                        "device_type": None, 
                        "ip": None, 
                        "device_id": None, 
                        "locale": None, 
                        "app_version": None 
                    }

    def __repr__(self):
        return f"""User(user_id={self.user_id}, """ \
                    f"""device_type={self.device_type}, """ \
                    f"""ip={self.masked_ip}, """ \
                    f"""device_id={self.masked_device_id}, """ \
                    f"""locale=[{self.locale}], """ \
                    f"""app_version={self.app_version}, """ \
                    f"""create_date={self.create_date})"""

    @staticmethod
    def create_user_login(js_obj: Dict[str]) -> Optional[UserLogin]:
        # TODO: Add more rigorous validations.
        # There's also probably a better way to test that the js_obj is what we
        # need.
        if js_obj.keys() != UserLogin.KEYS.keys():
            return None
        
        return UserLogin(
            user_id = js_obj.get("user_id"),
            device_type = js_obj.get("device_type"),
            masked_ip = data_mask.mask(js_obj.get("ip"), "masked_ip"),
            masked_device_id = data_mask.mask(js_obj.get("device_id"), "device_id"),
            locale = js_obj.get("locale"),
            app_version = js_obj.get("app_version").split(".")[0],
            create_date = datetime.now()
        )




def fetch_next_user(data: Dict[str]) -> Optional[UserLogin]:
    return json.loads(data, object_hook=UserLogin.create_user_login)