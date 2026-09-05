from django.db import models


class Sale(models.Model):

    order_id = models.CharField(
        max_length=50,
        unique=True
    )

    order_date = models.DateField()

    customer_name = models.CharField(
        max_length=100
    )

    product_name = models.CharField(
        max_length=100
    )

    category = models.CharField(
        max_length=100
    )

    region = models.CharField(
        max_length=50
    )

    quantity = models.IntegerField()

    sales_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    profit = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return self.order_id