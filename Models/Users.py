from . import Base, metadata
import sqlalchemy as sa


class User(Base):
    __table__ = sa.Table("User", metadata)

