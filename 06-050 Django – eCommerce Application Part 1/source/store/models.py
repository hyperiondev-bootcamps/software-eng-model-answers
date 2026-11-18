from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Store(models.Model):
    """
    Represents an independent vendor storefront.
    """
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stores')

    def __str__(self):
        return f"{self.name} (Owner: {self.owner.username})"


class Product(models.Model):
    """
    Represents an item listed for sale within a vendor store.
    Includes custom permissions for product operations.
    """
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        permissions = [
            ("add_products", "Can add products"),
            ("change_products", "Can change products"),
            ("delete_products", "Can delete products"),
            ("view_products", "Can view products"),
        ]

    def __str__(self):
        return self.name


class Review(models.Model):
    """
    Represents customer feedback and star ratings submitted by buyers.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.author.username} on {self.product.name} ({self.rating}/5)"


class ResetToken(models.Model):
    """
    Stores cryptographically secure, time-sensitive tokens for password resets.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
    expiry_date = models.DateTimeField()
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"ResetToken for {self.user.username} (Used: {self.used})"
