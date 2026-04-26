from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, text
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    rating = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))

