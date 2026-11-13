from no_discount import NoDiscount
from percentage_discount import PercentageDiscount
from bulk_discount import BulkDiscount
from student_discount import StudentDiscount

print(NoDiscount().apply(250))
print(PercentageDiscount(10).apply(250))
print(BulkDiscount(200, 20).apply(250))
print(StudentDiscount().apply(250))