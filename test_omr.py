from model import Batch,OrderLine
from unittest import TestCase
import pytest

from test_domain_try.model import Order

@pytest.fixture
class session():
    pass

class Test_ORM(TestCase):
    def test_orderline_mapper_can_load_lines(session):
        session.execute(
            'INSERT INTO orderline(sku,order_id,quantity) VALUES'
            '("order1", "RED-CHAIR", 12),'
            '("order1", "RED-TABLE", 13),'
            '("order2", "BLUE-LIPSTICK", 14)'
        )
        Expectec=[
            OrderLine("order1", "RED-CHAIR", 12),
            OrderLine("order1", "RED-TABLE", 13),
            OrderLine("order2", "BLUE-LIPSTICK", 14)
        ]
        assert session.query(OrderLine).all()==Expectec

    def test_orderline_mapper_can_save_line(session):
        new_line = OrderLine('order1','DECORATIVE-WIDGET',10)
        session.add(new_line)
        session.commit()
        lines = list(session.execute(
            'SELECT order_id, sku, qty FROM "order_line"'
        ))
        assert lines == [('order1','DECORATIVE-WIDGET',10)]
