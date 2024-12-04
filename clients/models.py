from django.db import models
from calendarapp.models.event import Package, Event, PackageType
from django.core.validators import RegexValidator

class Client(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=500)  # Adding max_length
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=11,  # Ensure the phone number doesn't exceed 11 digits
        validators=[
            RegexValidator(
                regex=r'^\d{1,11}$',
                message="Phone number must be up to 11 digits and numeric only.",
            )
        ],
    )
    preferred_time = models.TextField(null=True, blank=True, max_length=500) 
    is_member = models.BooleanField(default=False)

    # Many-to-many with Class through Registration
    classes = models.ManyToManyField(Event, through='Registration', related_name="clients")

    def __str__(self):
        return self.name


class Registration(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('TOTAL', 'Total Payment'),
        ('PARTIAL', 'Partial Payment'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('VISA', 'Visa'),
        ('CASH', 'Cash'),
        ('INSTAPAY', 'Instapay'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="registrations")
    class_obj = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    package_type = models.ForeignKey(PackageType, on_delete=models.SET_NULL, null=True)
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES,null=True)  # New Field
    price_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_left = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    classes_attended = models.PositiveIntegerField(default=0)
    classes_left = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        # Calculate the price left based on package price and payment type
        total_price = self.package.get_price(self.client.is_member)
        self.classes_left = self.package.number_of_sessions - self.classes_attended
        self.price_left = total_price - self.price_paid
        if not hasattr(self, '_force_manual_update'):
            self.classes_left = self.package.number_of_sessions - self.classes_attended
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Registration: {self.client.name} - {self.class_obj.name}"
