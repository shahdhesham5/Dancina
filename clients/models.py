from django.db import models
from calendarapp.models.event import Package, Event


class Client(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    note = models.TextField(null=True, blank=True)
    preferred_time = models.CharField(max_length=100, null=True, blank=True)  # For private classes
    is_member = models.BooleanField(default=False)

    # Many-to-many with Class through Registration
    classes = models.ManyToManyField(Event, through='Registration', related_name="clients")

    def __str__(self):
        return self.name


class Registration(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="registrations")
    class_obj = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True)
    payment_type = models.CharField(max_length=20, choices=[('TOTAL', 'Total Payment'), ('PARTIAL', 'Partial Payment')])
    price_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_left = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    classes_attended = models.PositiveIntegerField(default=0)
    classes_left = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        # Calculate the price left based on package price and payment type
        total_price = self.package.get_price(self.client.is_member)
        self.classes_left = self.package.number_of_sessions - self.classes_attended
        if self.payment_type == 'TOTAL':
            self.price_left = 0
        else:
            self.price_left = total_price - self.price_paid
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Registration: {self.client.name} - {self.class_obj.name}"