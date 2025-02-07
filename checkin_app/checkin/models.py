from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from geopy.distance import geodesic
from decimal import Decimal, ROUND_HALF_UP

# User model
class User(AbstractUser):
    is_checked_in = models.BooleanField(default=False)  # Add is_checked_in flag

# Workplace model with geolocation fields
class Workplace(models.Model):
    name = models.CharField(max_length=100)
    location = models.TextField()
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)

    def __str__(self):
        return self.name

# Attendance log model
class AttendanceLog(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE, db_index=True)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    checkin_latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    checkin_longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)

    def hours_worked(self):
        if self.check_in_time and self.check_out_time:
            return (self.check_out_time - self.check_in_time).total_seconds() / 3600
        return None

    def clean(self):
        if self.checkin_latitude:
            self.checkin_latitude = Decimal(self.checkin_latitude).quantize(Decimal('1.00000000'), rounding=ROUND_HALF_UP)
            if self.checkin_latitude < -90 or self.checkin_latitude > 90:
                raise ValidationError('Invalid latitude value')
        if self.checkin_longitude:
            self.checkin_longitude = Decimal(self.checkin_longitude).quantize(Decimal('1.00000000'), rounding=ROUND_HALF_UP)
            if self.checkin_longitude < -180 or self.checkin_longitude > 180:
                raise ValidationError('Invalid longitude value')
        if self.check_in_time and self.check_out_time and self.check_out_time <= self.check_in_time:
            raise ValidationError('Check-out time must be after check-in time')
        self.validate_location()

    def validate_location(self):
        if self.checkin_latitude and self.checkin_longitude:
            user_location = (float(self.checkin_latitude), float(self.checkin_longitude))
            workplace_location = (float(self.workplace.latitude), float(self.workplace.longitude))
            distance = geodesic(user_location, workplace_location).meters
            # Print statements for debugging
            if distance > 100:  # Temporarily increase the allowed distance to 100m for debugging
                raise ValidationError('You are not at the correct location.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Call full_clean to run validations
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.username} - {self.workplace.name}"