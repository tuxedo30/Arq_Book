# from ast import Try
# from msilib.schema import Error
# from re import L
from unittest import TestCase
import exceptions
import pytest
from model import Batch,OrderLine, Order
from datetime import date,tomorrow
from function_allocates_try import allocate #allocation_function, extract_lines, allocate, whereisallocated
from typing import List
from pytest import raises

def test_prefers_current_stock_batch_to_shipments(): #batches:List(Batch)):
    # Hice el método xd currect_stock= list(Batch)
    # for b in batches:
    #     if b.eta == None:
    #         currect_stock.append(b)
    # return currect_stock
    in_stock_batch=Batch("in-stock-batch","RETRO-CLOCK", 100,eta=None) #Fine
    shipment_batch=Batch("in-shipment-batch","RETRO-CLOCK",100,eta=tomorrow)
    line = OrderLine ("line000",10,"RETRO-CLOCK")
    allocate(line, [in_stock_batch,shipment_batch])
    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100

def test_prefers_earlier_batches():
    earliest=Batch("faster-batch","RETRO-LAMP",100,eta=date.today())
    medium=Batch("medium-batch","RETRO-LAMP", 100, eta=tomorrow)
    lastest=Batch("lastest-batch", "RETRO-LAMP",100,eta=date(3000,1,1))
    line = OrderLine("line001",100, "RETRO-LAMP")
    allocate(line,[earliest,medium,lastest])
    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert lastest.available_quantity == 100


# def test_allocation_earlier_date():
#     lines=set(OrderLine)
#     # lines.add(Order("CHAIR",1))
#     # lines.add(Order("TABLE",2))
#     lines.add(OrderLine("LAMP-NEON",3))
#     # order = Order("order-000",lines)
#     batch_early=Batch("ABC","LAMP-NEON",20,eta=date.today())
#     batch_late=Batch("XYZ","LAMP-NEON",20,eta=tomorrow)
#     allocation_function(batch_early,batch_late)
#     assert batch_early.available_quantity == 17 & batch_late.available_quantity == 20

def test_returns_allocated_batch_ref():
    batch_shipment = Batch("return-ref","MINIMALIST-SPOON",20,eta=date.today())
    batch_stock = Batch("return-ref","MINIMALIST-SPOON",20,eta=None)
    line=OrderLine("order-id","MINIMALIST-SPOON", 10)
    ref_batch = allocate(line,[batch_shipment,batch_stock])
    assert ref_batch == batch_shipment.reference

# def test_Extract_OrderLines():
#     lines=set(OrderLine)
#     lines.add(OrderLine("CHAIR",1))
#     lines.add(OrderLine("TABLE",2))
#     lines.add(OrderLine("LAMP-NEON",3))
#     order = Order("order-000",lines)
#     lines= extract_lines(Order)
#     # etc

def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch_still_on_stock=Batch("batch000","CHAIR-MATE",10,eta=date.today())
    line=OrderLine("order000","CHAIR-MATE", 10)
    allocate(line, [batch_still_on_stock])
    with pytest.raises(exceptions.OutOfStock, match="CHAIR-MATE"):
        allocate(OrderLine("order000","CHAIR-MATE", 1),[batch_still_on_stock])
    # try:
    #     allocate(line, [batch_out_of_stock])
    # except Error as e:
    #     print(e)

