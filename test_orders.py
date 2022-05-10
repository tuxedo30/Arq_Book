from unittest import TestCase
from datetime import date
from model import OrderLine
from model import Batch
from model import extract_OrdersLines
from model import warehouseStock

class test_Order(TestCase):

    def test_json_with_orders_lines_comes_to_order(self, jsonOrder):
        jsonOrder = {"OrderLine1":{
            "SKU" : "SMALL-TABLE",
            "Quantity" : 20
        }, "OrderLine2":{
            "SKU" : "RED-CHAIR",
            "Quantity" : 20
        }}
        OL = extract_OrdersLines(jsonOrder)
        assert OL["OrderLine1"] == ("jsonOrder","SMALL-TABLE", 20, date.today()) \
        & OL["OrderLine2"] == ("jsonOrder","RED-CHAIR", 20, date.today())

class test_batch(TestCase):
    def test_allocating_to_a_batch_reduces_the_available_quantity():
        batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
        line = OrderLine('order-ref', "SMALL-TABLE", 2)
        batch.allocate(line)
        assert batch.available_quantity == 18

    def test_not_possible_allocate_batch_less_quantity_than_order():
        batch = Batch("batch-002", "SMALL-TABLE", qty=20, eta=date.today())
        line2=OrderLine('order-ref0', "SMALL-TABLE", 22)
        batch.allocate(line2)
        assert batch.available_quantity == 20

    def test_order_line_in_the_same_batch():
        batch = Batch("batch-003", "SMALL-TABLE", qty=20, eta=date.today())
        line3=OrderLine('order-ref1', "SMALL-TABLE", 2)
        batch.allocate(line3)
        batch.allocate(line3)
        assert batch.available_quantity == 18
    
class test_ETA():
    def test_eta_is_earlier():
        warehouse_stock = warehouseStock()
        batch = Batch("batch-003", "SMALL-TABLE", qty=20, eta=date.today())
        batch2 = Batch("batch-004", "SMALL-TABLE", qty=20, eta=(date.today() + date.day(1)))
        warehouse_stock.allocate(batch)
        warehouse_stock.allcate(batch2)
        assert warehouse_stock.orderAllocation == ("batch-003","batch-004")

