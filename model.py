from datetime import date,datetime
from dataclasses import dataclass
from typing import Union, Optional,List,Set
import exceptions
from test_domain_try.exceptions import OutOfStock
# from pyparsing import Or

class Order():
    def __init__(self, order_reference: str, OrderLines:Set) -> None:
        self.order_reference = order_reference
        self.OrderLines = OrderLines
    

@dataclass(frozen=True) #value object should be inmutable
class OrderLine():
    sku: str
    qty: int
    Orderid: str


class Batch():
    def __init__(self, ref:str, sku: str, qty:int, eta: Union[date,None]):
        self.reference=ref
        self.sku=sku
        self._purchased_quantity=qty
        self.eta=eta
        self._lines_allocated = set() #A set because the items of a set are unique
    
    # def getReference(self):
    #     return self.__reference
    # def setReference(self, newR):
    #     self.__reference = self.__reference #This is tha hash value, should be inmutable


    def __eq__(self,other):
        if not isinstance(other, Batch):
            return False
        return self.__reference==other.__reference
    
    def __hash__(self):
        return hash(self.__reference)

    def __gt__(self,other):
        if self.eta==None:
            return False
        if other.eta==None:
            return True
        return self.eta > other.eta

    @property
    def allocated_quantity(self)->int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self)->int:
        return self._purchased_quantity - self.allocated_quantity

    def allocation(self, line: OrderLine):
        if self.can_allocate:
            self._lines_allocated.add(line)

    def can_allocate(self, ol: OrderLine)->bool:   
        is_idemp = False
        if (ol.Orderid in self._lines_allocated):
            is_idemp = True
        return ol.sku == self.sku & ol.qty <= self.available_quantity & is_idemp==False; 
            
    def deallocate(self, ol:OrderLine):
        if ol in self._lines_allocated:
            self._lines_allocated.remove(ol)


#-----------------------------------function allocation ---------------------------------
def allocate(line:OrderLine,List:Batch)->str:
    try:
        batch = next(b for b in sorted(List) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f'Product with sku {line.sku} is out of stock')
    