from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = String(100, nullable=False)

    def __repr__(self):        
        return f"<Item(name='{self.name}')>"