from model import Batch, OrderLine, Order
from typing import List,Set,Optional
from datetime import date

# def allocation_function(batches:List(Batch), orders:List(OrderLine)):
#     pass

# def extract_lines():
#     pass

def allocate(line:OrderLine,List:Batch)->str:
    batch = next(b for b in sorted(List) if b.can_allocate(line))
    batch.allocate(line)
    return batch.reference

    # #menor_eta:Optional[date]
    # ref=""
    # listSorted = sorted(List,key=lambda batch: batch.eta)
    # listSorted[0].allocation(line)
    # ref = listSorted[0].reference
    # # for b in List:
    # #     if (line.sku == b.sku):
    # #         if (b.eta == None):
    # #             b.allocate(line)
    # #             ref = b.reference
    # #         else:
    # #             pass

    # return ref