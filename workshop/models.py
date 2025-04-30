from django.db import models

class Owner(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Vehicle(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="vehicles")
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    license_plate = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"

class RepairHistory(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="repair_histories")
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f"Repair on {self.date} for {self.vehicle}"

class MaintenanceSchedule(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="maintenance_schedules")
    maintenance_type = models.CharField(max_length=200)
    scheduled_date = models.DateField()
    completed = models.BooleanField(default=False)
    completion_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.maintenance_type} on {self.scheduled_date} for {self.vehicle}"
