from unittest import getTestCaseNames
import repository
from model import Batch, OrderLine, allocate
from datetime import date

from test_domain_try.model import Order

def test_repository_can_save_batch(session):
    batch = Batch("batch0","RUSTY-SOAPDISH",30,eta=None)
    batch_repo = repository.SqlAlchemyRepository(session)
    batch_repo.add(batch)
    session.commit()
    batch_norepo = list(session.execute('SELECT reference, sku, _purchased_quantity, eta FROM "batch"'))
    assert batch_norepo == [("batch0","RUSTY-SOAPDISH",30,None)]

# def test_repository_can_consult_batch(session):
#     pass

def insert_order_line(session):
    session.execute('INSERT INTO order_line(order_id,sku, qty)'
    'VALUES ("order1", "GENERIC-SOFA",12)'
    )

    [[orderline_id]]=session.execute('SELECT id FROM order_line'
    'WHERE order_id=:order_id AND sku=:sku',
    dict(order_id='order1',sku="GENERIC-SOFA"),
    )

    return orderline_id

def insert_batch(session, batch_id):
    
    session.execute('INSERT INTO batch(reference,sku, _purchased_quantity, eta)'
    'VALUES (id=:batch_id, "GENERIC-SOFA", 20, null)'
    )

    [[batch_id]]=session.execute('SELECT id FROM batch'
    'WHERE reference=:batch_id AND sku="GENERIC-SOFA"',
    dict(batch_id=batch_id),
    )

    return batch_id

def insert_allocation(session, batch_id, orderline_id):
    session.execute('INSERT INTO allocation(batch_id, order_line_id)'
    'VALUES(:batch_id,:orderline_id)',
    dict(batch_id=batch_id,orderline_id=orderline_id),
    )

def test_repository_can_retrieve_batch_with_allocations(session):
    batch_repo = repository.SqlAlchemyRepository(session)
    expectect=Batch("batch1","GENERIC-SOFA", 8, None)
    #batchTwo=Batch("batch2","GENERIC-SOFA", 20, eta=date.Today())
    # line = OrderLine("order1",2,"GENERIC-SOFA")
    # batch_id = allocate(line, [batchOne,batchTwo])
    batch1= insert_batch(session,"batch1")
    insert_batch(session,"batch2")
    line1=insert_order_line(session)
    insert_allocation(session, batch1,line1)
    retrieve=batch_repo.get("batch1")
    #batch_from_get = set(batch_repo.get(Batch)
    assert expectect == retrieve
    assert  expectect.sku == retrieve.sku
    assert expectect._lines_allocated == {OrderLine("order1", "GENERIC-SOFA",12),}
