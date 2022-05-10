from unittest import TestCase
import model
from datetime import date

class test_batch(TestCase):

    def make_batch_and_line(self, sku, batch_qty, line_qty):
        return (
            model.Batch("batch-000", sku, batch_qty, eta=date.today()),
            model.OrderLine("order-000",sku, line_qty)
        )

    def test_can_allocate_Batch_quantity_more_Line_quantity(self):
        large_batch,small_line = self.make_batch_and_line("SMALL-TABLE", 20, 2)
        assert large_batch.can_allocate(small_line)

    def test_cannot_allocate_Batch_quatity_less_Line_quantity(self):
        small_batch,large_line = self.make_batch_and_line("SMALL-TABLE", 2, 20)
        assert small_batch.can_allocate(large_line) is False

    def test_can_allocate_Batch_quatity_iqual_Line_quantity(self):
        iqual_batch,iqual_line = self.make_batch_and_line("SMALL-TABLE", 2, 2)
        assert iqual_batch.can_allocate(iqual_line)

    def test_Batch_sku_should_be_iqual_sku_Line():
        batch = model.Batch ("batch-000", "PRODUCT", 3, eta =None)
        different_sku_line = model.OrderLine ("OTHER-PRODUCT", 2, "order-000")
        assert batch.can_allocate(different_sku_line) is False

    def test_cannot_deallocate_unallocate_line(self):
        batch, unallocated_line = batch("DECORATIVE-TRINKET",20,2)
        batch.deallocate(unallocated_line)
        assert batch.available_quantity == 20
    
    def test_allocation_is_idempotent(self):
        batch, line = self.make_batch_and_line("COMPUTER-TABLE", 12, 10)
        batch.allocation(line)
        batch.allocation(line)
        assert batch.available_quantity == 18
        #assert batch.can_allocate(line) is False
