from django import forms
from .models import Voitures, Manager


class VoitureForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = Voitures
        fields = ['nom_voiture', 'description', 'prix', 'image']

class ReservationForm(forms.ModelForm):
    numero_client = forms.CharField(label='Numéro du client')
    date_reservation = forms.DateField(label='Date de réservation')
    status = forms.ChoiceField(
        label='Traiter la demande',
        choices=[
            ('accepted', 'Accepter'),
            ('rejected', 'Refuser')
        ]
    )
    id_voiture = forms.CharField(widget=forms.HiddenInput())

    # Optional: Add any additional form validation or custom logic here

class ManagerForm(forms.ModelForm):
    class Meta:
        model = Manager
        fields = ['username', 'email', 'password']
