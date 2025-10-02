from ..database import database
from sqlalchemy import Integer, Column, String, TIMESTAMP, ForeignKey, func
import json
from . import User

class Integration(database.Base):
    __tablename__ = "Integration"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.User.id))
    api_key = Column(String)
    app = Column(String)
    type = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class Integration_credentials(database.Base):
    __tablename__ = "integration_credentials"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.User.id))
    app = Column(String)
    store_name = Column(String)
    client_key = Column(String)
    client_secret = Column(String)
    base_url = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class WooIntegration(database.Base):
    __tablename__ = "Woo_Integration"
    id = Column(Integer, primary_key=True)
    integration_id = Column(Integer, ForeignKey(Integration.id))
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey(User.User.id))
    api_key = Column(String, nullable=True)
    rest_key = Column(String, nullable=True)
    rest_secret = Column(String, nullable=True)
    type = Column(String)
    template = Column(String)
    template_data = Column(String)
    parameters = Column(String)  # JSON string
    repeat_days = Column(String, nullable=True)  # JSON string
    time = Column(String, nullable=True)
    product_id = Column(Integer, nullable=True)
    status = Column(String, nullable=True)
    base_url = Column(String, nullable=True)
    image_id = Column(String, nullable=True)

    def set_parameters(self, params):
        self.parameters = json.dumps(params)

    def get_parameters(self):
        return json.loads(self.parameters or "[]")

    def set_repeat_days(self, days):
        self.repeat_days = json.dumps(days)

    def get_repeat_days(self):
        return json.loads(self.repeat_days or "[]")
