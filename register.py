from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///stronger.db', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    # def __init__(self, username, password):
    #     """"""
    #     self.username = username
    #     self.password = password

    def __repr__(self):
        return "<User(username={}, password={})>" \
            .format(self.username, self.password)

class User_reg(Base):
    __tablename__ = "all_users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    confirm = Column(String)

    # def __init__(self, name, username, email, password, confirm):
    #     """"""
    #     self.name = name
    #     self.username = username
    #     self.email = email
    #     self.password = password
    #     self.confirm = confirm

    def __repr__(self):
        return "<User_reg(name={}, username={}, email={}, password={}, confirm={})>" \
            .format(self.name, self.username, self.email, self.password, self.confirm)

# Create tables
Base.metadata.create_all(engine)
