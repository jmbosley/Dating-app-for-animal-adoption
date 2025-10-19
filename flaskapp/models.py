from flaskapp import db
import sqlalchemy as sa  # comes with types like String
from sqlalchemy.orm import Mapped, mapped_column # type hints


# create a new model
# optional read: https://www.geeksforgeeks.org/python/sqlalchemy-orm-declaring-mapping/
# https://stackoverflow.com/questions/76498857/what-is-the-difference-between-mapped-column-and-column-in-sqlalchemy
class publicAccount(db.Model):
    __tablename__ = 'publicAccounts'
    # attributeName: typehint = mapped_column(sql specifications)
    idPublicAccounts: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    firstName: Mapped[str] = mapped_column(sa.String(45))
    lastName: Mapped[str] = mapped_column(sa.String(45))
    email: Mapped[str] = mapped_column(sa.String(45))  # can set unique=true later
    phoneNumber: Mapped[str] = mapped_column(sa.String(45))
    password: Mapped[str] = mapped_column(sa.String(45))


class adminAccount(db.Model):
    __tablename__ = 'adminAccounts'
    # attributeName: typehint = mapped_column(sql specifications)
    idAdminAccounts: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    firstName: Mapped[str] = mapped_column(sa.String(45))
    lastName: Mapped[str] = mapped_column(sa.String(45))
    email: Mapped[str] = mapped_column(sa.String(45))  # can set unique=true later
    phoneNumber: Mapped[str] = mapped_column(sa.String(45))
    password: Mapped[str] = mapped_column(sa.String(45))

