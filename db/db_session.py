from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

#Home IP
#DATABASE_URL = "postgresql://postgres:admin@192.168.0.152:5432/relationdata"

#AAU IP
DATABASE_URL = "postgresql://postgres:admin@169.254.155.152:5432/relationdata"

Base = declarative_base()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency function
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()