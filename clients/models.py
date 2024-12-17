from django.db import models
from calendarapp.models.event import Package, Event, PackageType, ClassOccurrence
from django.core.validators import RegexValidator
import uuid
from django.utils.timezone import now
from datetime import datetime
from django.db import transaction
    
class Client(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=500) 
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=11,  
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

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="registrations")
    class_obj = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    package_type = models.ForeignKey(PackageType, on_delete=models.SET_NULL, null=True)
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    price_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_left = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    classes_attended = models.PositiveIntegerField(default=0)
    classes_left = models.PositiveIntegerField()
    registration_date = models.DateTimeField(auto_now_add=True, null=True)
    expiration_date = models.DateTimeField(db_index=True, null=True)

    def save(self, *args, **kwargs):
        if not self.registration_date:
            self.registration_date = now()
            
        is_new = self.pk is None 
        # Calculate the price left based on package price and payment type
        if is_new and not self.expiration_date:  # Only calculate price_left for new instances
            self.expiration_date = self.registration_date + self.package.duration
            total_price = self.package.get_price(self.client.is_member)
            self.classes_left = self.package.number_of_sessions - self.classes_attended
            self.price_left = total_price - self.price_paid
            if not hasattr(self, '_force_manual_update'):
                self.classes_left = self.package.number_of_sessions - self.classes_attended
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Registration: {self.client.name} - {self.class_obj.name}"

def generate_receipt_number():
    return f"DNC-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"


class TransactionSettings(models.Model):
    starting_receipt_number = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Transaction Settings (Starting Receipt Number: {self.starting_receipt_number})"

    
class Transaction(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('VISA', 'Visa'),
        ('CASH', 'Cash'),
        ('INSTAPAY', 'Instapay'),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="transactions")
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name="transactions_registration", null=True, blank=True)
    value_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES,null=True) 
    date = models.DateTimeField(default=now)
    receipt_number = models.PositiveIntegerField(unique=True)  # Sequential and unique

    def save(self, *args, **kwargs):
        if not self.receipt_number:  # Only generate receipt_number if not already set
            with transaction.atomic():
                # Lock the settings row to prevent race conditions
                settings = TransactionSettings.objects.select_for_update().first()
                if not settings:
                    settings = TransactionSettings.objects.create(starting_receipt_number=1)

                self.receipt_number = settings.starting_receipt_number
                settings.starting_receipt_number += 1  # Increment for the next transaction
                settings.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transaction: {self.client.name} - Receipt {self.receipt_number}"


class Attendance(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="attendances")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="attendances")
    # class_occurrence = models.ForeignKey(ClassOccurrence, on_delete=models.CASCADE, related_name="attendances")
    attendance_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Attendance: {self.client.name} for {self.event.name} "

