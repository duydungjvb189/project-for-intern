from sqlalchemy import String, Integer, Column
from models.user_model import Base

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    def __repr__(self):        
        return f"<Item(name='{self.name}')>"