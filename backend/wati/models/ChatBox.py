from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, BIGINT
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from ..database import database

class Conversation(database.Base):
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True, index=True)
    wa_id = Column(String, index=True)
    message_id = Column(String)
    phone_number_id = Column(BIGINT)
    message_content = Column(Text)
    media_id = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    context_message_id = Column(String, nullable=True, default=None)
    message_type = Column(String)
    is_first_message = Column(Boolean, default=False)
    direction = Column(String, nullable=False)

class Last_Conversation(database.Base):
    __tablename__ = 'last_conversations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String)
    message_content = Column(Text)
    business_account_id = Column(String, nullable=False)
    sender_wa_id = Column(String, nullable=False)
    sender_name = Column(String, nullable=False)
    receiver_wa_id = Column(String, nullable=False)
    last_chat_time = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)

    def __init__(self, business_account_id, sender_wa_id, sender_name, receiver_wa_id, last_chat_time=None, message_content=None, message_id=None, active=True):
        self.business_account_id = business_account_id
        self.message_id = message_id
        self.message_content = message_content
        self.sender_wa_id = sender_wa_id
        self.sender_name = sender_name
        self.receiver_wa_id = receiver_wa_id
        self.last_chat_time = last_chat_time or datetime.now()
        self.active = active
