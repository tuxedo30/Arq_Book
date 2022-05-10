from repository import AbstractRepository
from test_domain_try.model import Batch
import ApiFlask


class FakeRepositoryforTest(AbstractRepository):
    def __init__(self):
        self._batches = set(Batch)
    
    def add(self, batch: Batch):
        self._batches.add(batch)

    def get(self, refer):
        return next(b for b in self._batches if b.reference == refer)
        #Is a way of simplify a for loop
        #The function next return the next element of a iterator; in this case the iterator is the set _batches
        #have like a kind of memory, and this is the because is used. No return the same element
    
    def list(self):
        return list(self._batches)

def test_api_can_save_batch():
    sessionFake = FakeRepositoryforTest()
    pass 

def test_api_can_retrieve_one_batch():
    pass

def test_api_can_retrieve_all_batch():
    pass