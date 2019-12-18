from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///stronger.db', echo=True)
Base = declarative_base()

class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('all_users.username'))
    sfwa_id = Column(Integer)
    yabook_id = Column(Integer)
    bookchor_id = Column(Integer)

    def __repr__(self):
        return "<Bookmark(user_id={}, sfwa_id={}, yabook_id={}, bookchor_id={})>" \
            .format(self.user_id, self.sfwa_id, self.yabook_id, self.bookchor_id)

class SFWA(Base):
    __tablename__ = "sfwa"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    image = Column(String)
    link = Column(String)

    def __repr__(self):
        return "<SFWA(name={}, image={}, link={})>" \
            .format(self.name, self.image, self.link)

class YABOOK(Base):
    __tablename__ = "yabook"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    image = Column(String)
    link = Column(String)

    def __repr__(self):
        return "<YABOOK(name={}, image={}, link={})>" \
            .format(self.name, self.image, self.link)

class BOOKCHOR(Base):
    __tablename__ = "bookchor"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    image = Column(String)
    link = Column(String)

    def __repr__(self):
        return "<BOOKCHOR(name={}, image={}, link={})>" \
            .format(self.name, self.image, self.link)

class User_reg(Base):
    __tablename__ = "all_users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    confirm = Column(String)

    def __repr__(self):
        return "<User_reg(name={}, username={}, email={}, password={}, confirm={})>" \
            .format(self.name, self.username, self.email, self.password, self.confirm)

# Create tables
Base.metadata.create_all(engine)
