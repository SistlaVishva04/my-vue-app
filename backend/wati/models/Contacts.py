from ..database import database
from sqlalchemy import Integer, Column, String, TIMESTAMP, ForeignKey, func
from . import User
import json

class Contact(database.Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(User.User.id))
    name = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String, index=True)
    tags = Column(String, default="[]")  # JSON string
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    def set_tags(self, tags_list):
        self.tags = json.dumps(tags_list)

    def get_tags(self):
        return json.loads(self.tags or "[]")
