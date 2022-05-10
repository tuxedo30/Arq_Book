import orm
from model import Batch
from abc import ABC, abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from test_domain_try.test_omr import session

def createSession():
    # engine = create_engine('mysql://scott:tiger@localhost')
    # session = sessionmaker(engine)
    return session

class AbstractRepository(ABC):
    @abstractmethod
    def add(self, batch: Batch):
        try:
            session.begin()
            session.add(batch)
        except:
            session.rollback()
            raise NotImplementedError
        else:
            session.commit()

    @abstractmethod
    def get(self, refer)-> Batch:
        try:
            batch=session.query(Batch).filter_by(reference=refer).all()
            return batch
        except:
            raise NotImplementedError

class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session
    
    def add(self, batch: Batch):
        self.session.add(batch)

    def get(self, refer):
        return session.query(Batch).filter_by(reference=refer).one()
    
    def list(self):
        return session.query(Batch).all()