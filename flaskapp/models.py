from flaskapp import db
from datetime import date
import sqlalchemy as sa  # comes with types like String
from sqlalchemy.orm import Mapped, mapped_column  # type hints


# create a new model
# optional read: https://www.geeksforgeeks.org/python/sqlalchemy-orm-declaring-mapping/
# https://stackoverflow.com/questions/76498857/what-is-the-difference-between-mapped-column-and-column-in-sqlalchemy
class publicAccount(db.Model):
    __tablename__ = 'publicAccounts'
    # attributeName: typehint = mapped_column(sql specifications)
    idPublicAccounts: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    firstName: Mapped[str] = mapped_column(sa.String(45))
    lastName: Mapped[str] = mapped_column(sa.String(45))
    email: Mapped[str] = mapped_column(sa.String(45))  # can set unique=true later (off for easier debugging)
    phoneNumber: Mapped[str] = mapped_column(sa.String(45), nullable = True) # no default specified: default NULL
    password: Mapped[str] = mapped_column(sa.String(45))


class adminAccount(db.Model):
    __tablename__ = 'adminAccounts'
    # attributeName: typehint = mapped_column(sql specifications)
    idAdminAccounts: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    firstName: Mapped[str] = mapped_column(sa.String(45))
    lastName: Mapped[str] = mapped_column(sa.String(45))
    email: Mapped[str] = mapped_column(sa.String(45))  # unique = true
    phoneNumber: Mapped[str] = mapped_column(sa.String(45), nullable = True)
    password: Mapped[str] = mapped_column(sa.String(45))


class animal(db.Model):
    __tablename__ = 'animals'
    # attributeName: typehint = mapped_column(sql specifications)
    idAnimals: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(45))
    birthday: Mapped[date]  = mapped_column(nullable = True)
    type: Mapped[str] = mapped_column(sa.String(45))
    breed: Mapped[str] = mapped_column(sa.String(45), nullable = True)
    disposition: Mapped[str] = mapped_column(sa.String(45), nullable = True)
    availability: Mapped[bool] = mapped_column(default=True)
    description: Mapped[str] = mapped_column(sa.String(300), default='')
    numImages: Mapped[int] = mapped_column(default = 0) # image naming convention: petImg_{id}_{imageNum}.jpg


class newsPost(db.Model):
    __tablename__ = 'newsPost'
    # attributeName: typehint = mapped_column(sql specifications)
    idNewsPosts: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(sa.String(100))
    body: Mapped[str] = mapped_column(sa.String(10000))
    datePublished: Mapped[date] = mapped_column(default=date.today())