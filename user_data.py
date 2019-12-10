from sqlalchemy.orm import sessionmaker
from register import *

engine = create_engine('sqlite:///stronger.db', echo=True)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

user = User_reg(name='name', username='username', email='email', password='password', confirm='confirm')
session.add(user)

session.commit()
