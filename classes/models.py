from django.db import models





# class Class(models.Model):
#     name = models.CharField(max_length=100)
#     interval = models.CharField(max_length=100)  # e.g., "Every Sunday, 2pm to 4pm"
#     instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, related_name="classes")
#     studio_location = models.ForeignKey(StudioLocation, on_delete=models.SET_NULL, null=True, related_name="classes")

#     def __str__(self):
#         return f"{self.name} ({self.interval})"


