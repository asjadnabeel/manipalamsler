from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.urls import reverse #Used to generate URLs by reversing the URL patterns

class Patient(models.Model):
    """
    Model representing a patient
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file.
    address = models.TextField(max_length=400, help_text="Enter a brief address of patient")
    age = models.IntegerField('AGE')
    contact_no = models.CharField(max_length=10, help_text="Select contact number")
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(blank=True,null=True,unique=True)
    fundus_photo = models.ImageField(upload_to="fundus/", null=True, blank=True)


    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s, %s' % (self.last_name, self.first_name)

    def get_absolute_url(self):
        """
        Returns the url to access a particular patient instance.
        """
        return reverse('patient-detail', args=[str(self.id)])

import uuid
class AmslerGrid(models.Model):

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular amsler grid")
    patient = models.ForeignKey('Patient', on_delete=models.SET_NULL, null=True)
    #imprint = models.CharField(max_length=200)
    verify_date = models.DateField(null=True, blank=True)

    amsler_score = models.IntegerField('Amsler_score')
    photo = models.ImageField(upload_to="img/", null=True, blank=True)
    grid1 = models.ImageField(upload_to="grid/", null=True, blank=True)


    STATUS = (
        ('v', 'Verified'),
        ('u', 'Unverified'),

    )

    status = models.CharField(max_length=1, choices=STATUS, blank=True, default='u', help_text='Amsler Grid Status')

    class Meta:
        ordering = ["verify_date"]

    def __str__(self):

        return  self.patient.first_name

    def get_absolute_url(self):

        #id_args = self.str(self.id)
        return reverse('amsler', args=[str(self.patient.id), str(self.uid)])


class Hospital(models.Model):
    """
    Model representing a hospital (e.g. AIIMS, KMC).
    """
    name = models.CharField(max_length=200, help_text="Enter a hospital name (e.g. KMC Manipal)")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

class Doctor(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=10, blank=True)
    hospital = models.ManyToManyField(Hospital, help_text="Select the hospital to which the doctor belongs", blank=True)
    username = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('doctor-detail', args=[str(self.id)])


    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s, %s' % (self.last_name, self.first_name)