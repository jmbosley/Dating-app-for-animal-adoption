from flaskapp import db
from datetime import date
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, WriteOnlyMapped, mapped_column, relationship


# create a new model
# optional read: https://www.geeksforgeeks.org/python/sqlalchemy-orm-declaring-mapping/
# https://stackoverflow.com/questions/76498857/what-is-the-difference-between-mapped-column-and-column-in-sqlalchemy
class publicAccount(db.Model):
    __tablename__ = 'publicAccounts'
    # attributeName: typehint = mapped_column(sql specifications)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    firstName: Mapped[str] = mapped_column(sa.String(45))
    lastName: Mapped[str] = mapped_column(sa.String(45))
    userName: Mapped[str] = mapped_column(sa.String(45))
    email: Mapped[str] = mapped_column(sa.String(45))  # can set unique=true later (off for easier debugging)
    phoneNumber: Mapped[str] = mapped_column(sa.String(45), nullable=True)  # no default specified: default NULL
    password: Mapped[str] = mapped_column(sa.String(45))
    numImages: Mapped[int] = mapped_column(default=0)  # image naming convention: accountImg_{{userName}}.jpg

    # can access with publicAccountObject.animals.select()
    animals: WriteOnlyMapped['animal'] = relationship(back_populates='publicAccount')


class adminAccount(db.Model):
    __tablename__ = 'adminAccounts'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    firstName: Mapped[str] = mapped_column(sa.String(45))
    lastName: Mapped[str] = mapped_column(sa.String(45))
    userName: Mapped[str] = mapped_column(sa.String(45))
    email: Mapped[str] = mapped_column(sa.String(45))  # unique = true
    phoneNumber: Mapped[str] = mapped_column(sa.String(45), nullable=True)
    password: Mapped[str] = mapped_column(sa.String(45))
    numImages: Mapped[int] = mapped_column(default=0)  # image naming convention: accountImg_{{userName}}.jpg



class animal(db.Model):
    __tablename__ = 'animals'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(45))
    birthday: Mapped[date]  = mapped_column(index=True, nullable=True)  # index for sorting purposes
    type: Mapped[str] = mapped_column(sa.String(45))
    breed: Mapped[str] = mapped_column(sa.String(45), nullable=True)
    availability: Mapped[str] = mapped_column(sa.String(45), default="Available")
    description: Mapped[str] = mapped_column(sa.String(300), default='')
    numImages: Mapped[int] = mapped_column(default=0)  # image naming convention: animalImg_{id}_{num <= numImages}.jpg
    # disposition: friendly with who?
    children: Mapped[bool] = mapped_column(default=False)
    dogs: Mapped[bool] = mapped_column(default=False)
    cats: Mapped[bool] = mapped_column(default=False)
    needsLeash: Mapped[bool] = mapped_column(default=False, nullable=True)

    idPublicAccount: Mapped[int] = mapped_column(sa.ForeignKey(publicAccount.id), index=True, nullable=True)

    newsPosts: WriteOnlyMapped['newsPost'] = relationship(back_populates='animal')

    # can access related publicAccount with foreign key or with animalObject.publicAccount
    publicAccount: Mapped['publicAccount'] = relationship(back_populates='animals')


class newsPost(db.Model):
    __tablename__ = 'newsPosts'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(sa.String(100))
    body: Mapped[str] = mapped_column(sa.String(10000))
    datePublished: Mapped[date] = mapped_column(default=date.today(), index=True)

    idAnimal: Mapped[int] = mapped_column(sa.ForeignKey(animal.id), index=True, nullable=True)

    # directly access related animal objects with newsPost.animal instead of selecting them with foreign id
    animal: Mapped['animal'] = relationship(back_populates='newsPosts')
