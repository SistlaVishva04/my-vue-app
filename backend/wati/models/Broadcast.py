from ..database import database
from sqlalchemy import Integer, Column, String, Boolean, TIMESTAMP, ForeignKey, func
import json
from . import User

class BroadcastList(database.Base):
    __tablename__ = "BroadcastList"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(User.User.id))
    name = Column(String)
    type = Column(String, nullable=True)
    template = Column(String)
    contacts = Column(String)  # JSON string

    success = Column(Integer)
    failed = Column(Integer)
    status = Column(String)
    scheduled_time = Column(TIMESTAMP, nullable=True)
    task_id = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    def set_contacts(self, contacts_list):
        self.contacts = json.dumps(contacts_list)

    def get_contacts(self):
        return json.loads(self.contacts or "[]")

class BroadcastAnalysis(database.Base):
    __tablename__ = "BroadcastAnalysis"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(User.User.id))
    broadcast_id = Column(Integer, ForeignKey(BroadcastList.id))
    status = Column(String)
    message_id = Column(String, unique=True)
    phone_no = Column(String)
    contact_name = Column(String)
    read = Column(Boolean, nullable=True)
    delivered = Column(Boolean, nullable=True)
    sent = Column(Boolean, nullable=True)
    replied = Column(Boolean, nullable=True)
    error_reason = Column(String, nullable=True)
