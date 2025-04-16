from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from eralchemy2 import render_er

Base = declarative_base()
db = SQLAlchemy()

class User(Base):  
    __tablename__ = 'user' 
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    people = relationship("People", backref="user")
    planets = relationship("Planet", backref="user")
    favorites = relationship("Favorite", backref="user")
    vehicles = relationship("Vehicle", backref="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class People(Base):  
    __tablename__ = 'people'  
    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    caption: Mapped[str] = mapped_column(String(500), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

class Planet(Base):  
    __tablename__ = 'planet'   
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

class Vehicle(Base):  
    __tablename__ = 'vehicle'   
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    model: Mapped[str] = mapped_column(String(120), nullable=True)
    manufacturer: Mapped[str] = mapped_column(String(120), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

class Favorite(Base): 
    __tablename__ = 'favorites'  
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=True)
    people_id: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicle.id"), nullable=True)

try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
