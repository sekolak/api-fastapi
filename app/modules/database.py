from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# For archive, this bloc give us possibility to connect a database without using sqlalchemy


#while True:

#    try:
#        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres', 
#                                cursor_factory=RealDictCursor)
#        cursor = conn.cursor()
#        print ("Database connection was succesfull !!")
#        break
#    except Exception as error:
#        print("Connection to database failed")
#        print("Error; ", error)
#        time.sleep(2)