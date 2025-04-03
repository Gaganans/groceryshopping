from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class GroceryItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    added_on = models.DateTimeField(auto_now_add=True)
    purchased = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    @property
    def total_cost(self):
        return self.quantity * self.price
    
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paypal_payment_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')  # e.g., 'pending', 'completed', 'failed'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.paypal_payment_id} - {self.status}"    