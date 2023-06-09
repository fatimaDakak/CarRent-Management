from audioop import reverse

from django.db import models
from django.shortcuts import redirect


# Create your models here.


class Admin(models.Model):
    id_admin = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def _str_(self):
        return self.username

class Client(models.Model):

    numero_client = models.AutoField(primary_key=True)
    nom_client = models.CharField(max_length=100)
    prenom_client = models.CharField(max_length=100)
    email_client = models.EmailField()

    def __str__(self):
        return f'{self.nom_client} {self.prenom_client}'
class Manager(models.Model):
    id_manager = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Voitures(models.Model):
    STATUS_CHOICES = [
        ('N', 'Not Reserved'),
        ('R', 'Reserved'),
    ]
    id_voiture = models.AutoField(primary_key=True)
    nom_voiture = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=100)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='N')

    def __str__(self):
        return self.nom_voiture

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('A', 'accepted'),
        ('R', 'rejected'),
    ]
    id_reservation = models.AutoField(primary_key=True)
    numero_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    id_manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    id_voiture = models.ForeignKey(Voitures, on_delete=models.CASCADE)
    date_reservation = models.DateField()
    status_reservation = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self):
        return str(self.id_reservation)

