from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Complaint(models.Model):

    title = models.CharField(max_length=200,null=False)

    description = models.TextField(null=False)

    COMPLAINT_TYPE_CHOICES = (
        ("CLEANLINESS","cleanliness"),
        ("STAFF BEHAVIOUR","staff behaviour"),
        ("WAITING TIME","waiting time"),
        ("BILLING","billing"),
        ("EQUIPMENT","equipment")
    )

    complaint_type = models.CharField(max_length=200,choices=COMPLAINT_TYPE_CHOICES)

    department = models.CharField(max_length=200)

    PRIORITY_CHOICES = (
        ("LOW","low"),
        ("MEDIUM","medium"),
        ("HIGH","high"),
        ("CRITICAL","critical")
    )

    priority = models.CharField(max_length=200,choices=PRIORITY_CHOICES,default="MEDIUM")

    STATUS_CHOICES = (
        ("SUBMITTED","submitted"),
        ("UNDER REVIEW","under review"),
        ("IN PROGRESS","in progress"),
        ("RESOLVED","resolved")
    )

    status = models.CharField(max_length=200,choices=STATUS_CHOICES,default="SUBMITTED")

    reported_date = models.DateField(auto_now_add=True)

    owner = models.ForeignKey(User,on_delete=models.CASCADE)