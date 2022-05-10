# #declarative mapping
# #declarative_base, registry
from sqlalchemy import Column,String, Integer, Date, ForeignKey, Table, MetaData
# from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import registry, relationship
from model import OrderLine, Batch, Order, allocate

# Base = declarative_base()

# class BatchDeclarative(Base):
#     __tablename__='batch'
#     red = Column(String)
#     sku =Column(String)
#     purcharsed_quantity = Column(Integer)
#     eta = Column(Date)
#     lines_alocated = Column(String)

# mapper_register = registry()
# Base2= mapper_register.generate_base()

#Imperative Mapping (Clasical)

mapper_register = registry()
metadata_onj = MetaData()

order_table = Table(
    'order',
    metadata_onj,
    Column('id',String(255), primary_key=True)
)

orderline_table = Table(
    'order_line',
    metadata_onj,
    Column('sku', String(255)),
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('qty', Integer, nullable=False),
    Column('order_id', String(255), ForeignKey('order.id')
    )
)

batch_table = Table(
    'batch',
    metadata_onj,
    Column('reference', String(255),
    Column('sku', String(255)),
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('_purchased_quantity', Integer, nullable=False),
    Column('eta',Date,nullable=True)
))

allocation=Table(
    'allocation',
    metadata_onj,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('order_line_id', Integer, ForeignKey('order_line.id')),
    Column('batch_id', Integer, ForeignKey('batch.id'))
)


def start_mapping():
    mapper_register.map_imperatively(Order, order_table, properties={
        'orderlines': relationship(OrderLine, backref='order', order_by=orderline_table.c.order_id)
    })
    mapper_register.map_imperatively(OrderLine, orderline_table, properties={
        'allocations': relationship(allocate, backref='order_line', order_by=allocation.c.order_line_id)
    })
    
    mapper_register.map_imperatively(Batch, batch_table, properties={
        'allocations': relationship(allocate, backref='batch', order_by=allocation.c.batch_id)
    })