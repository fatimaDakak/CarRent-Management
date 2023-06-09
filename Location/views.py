from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.core.files.storage import FileSystemStorage, default_storage
from django.conf import settings
from Location.forms import VoitureForm, ReservationForm, ManagerForm
from Location.models import Manager, Voitures, Reservation, Client, Admin
import os
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse, Http404
from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect


def manager_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        print(password)
        try:
            manager_obj = Manager.objects.get(email=email, password=password)
            # Successful login, store manager ID in session and redirect to manager home page
            request.session['id_manager'] = manager_obj.id_manager
            print(manager_obj.id_manager)

            return redirect('manager_home')
        except Manager.DoesNotExist:
            # Email or password is incorrect, show error message
            messages.error(request, 'Invalid email or password.')

    return render(request, 'Manager/login_manager.html')


def manager_home(request):
    if 'id_manager' in request.session:
        id_manager = request.session['id_manager']
        if request.method == 'POST':
            form = VoitureForm(request.POST, request.FILES)
            if form.is_valid():
                voiture = form.save(commit=False)
                # Save the voiture instance
                voiture.save()

                # Get the uploaded image file
                image = request.FILES['image']

                # Generate the file path to save in the static/images folder
                file_path = os.path.join(settings.STATIC_ROOT, 'images', image.name)

                # Save the image to the static/images folder
                default_storage.save(file_path, image)

                # Generate the URL for the image
                image_url = os.path.join(settings.STATIC_URL, 'images', image.name)

                # Update the voiture instance with the image URL
                # Update the voiture instance with the corrected image path
                voiture.image = image_url.replace('\\', '/')
                voiture.save()

                return redirect('manager_home')  # Redirect to GET request after successful POST

        else:
            form = VoitureForm()

        clients = Client.objects.all()
        voitures = Voitures.objects.filter(status='N')
        context = {
            'voitures': voitures,
            'form': form,
            'clients': clients,
            'id_manager': id_manager
        }
        return render(request, 'Manager/list_annonces.html', context)
    else:
        return redirect('manager_login')



def reservation_reçus(request):
    reservations = Reservation.objects.all()
    context = {'reservations': reservations}
    return render(request, 'Manager/reservations.html', context)


def logout_view(request):
    logout(request)
    response = redirect('manager_login')  # Redirect to the login page after logout

    # Clear session data
    request.session.flush()

    # Prevent caching
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response
def list_clients(request):
    clients = Client.objects.all()
    for client in clients:
        print(client)
    context = {'clients': clients}
    return render(request, 'Manager/list_clients.html', context)


def ajouter_client(request):
    if request.method == 'POST':
        nom_client = request.POST['nom_client']
        prenom_client = request.POST['prenom_client']
        email_client = request.POST['email_client']

        client = Client(nom_client=nom_client, prenom_client=prenom_client,
                        email_client=email_client)
        client.save()

        return redirect(list_clients)

    return render(request, 'ajouter_client.html')

from django.views.decorators.http import require_http_methods


def supprimer_client(request, numero_client):
    if request.method == 'GET':
        try:
            client = Client.objects.get(numero_client=numero_client)
            reservations = Reservation.objects.filter(numero_client=client.numero_client)
            client.delete()
            reservations.delete()
            return redirect('list_clients')
        except Client.DoesNotExist:
            return HttpResponseNotAllowed(['GET'])

    return HttpResponseNotAllowed(['GET'])



def make_reservation(request):
    if request.method == 'POST':
        numero_client = request.POST.get('numero')
        date_reservation = request.POST.get('date_reservation')
        id_manager = request.POST.get('id_manager')
        status = request.POST.get('status')
        id_voiture = request.POST.get('id_voiture')
        print(status)

        # Retrieve the Client, Manager, and Voiture instances
        client = Client.objects.get(numero_client=numero_client)
        manager = Manager.objects.get(id_manager=id_manager)
        voiture = Voitures.objects.get(id_voiture=id_voiture)
        # Create a new Reservation instance
        reservation = Reservation.objects.create(
            numero_client=client,
            id_manager=manager,
            date_reservation=date_reservation,
            status_reservation=status,
            id_voiture=voiture
        )
    # Update the voiture status if the reservation is accepted
        if status == 'A':
            Voitures.objects.filter(id_voiture=id_voiture).update(status='R')

    return redirect('manager_home')


#admin

def admin_home(request):

    if request.method == 'POST':
        form = ManagerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_home')
    else:
        form = ManagerForm()

    managers = Manager.objects.all()
    context = {'managers': managers, 'form': form}
    return render(request, 'Admin/list_managers.html', context)

def modifier_mana(request,username):
    return render(request, 'Admin/modifier.html')


def liste_managers(request):
    managers = Manager.objects.all()
    return render(request, 'Admin/list_managers.html', {'managers': managers})

def modifier_manager(request, id_manager):
    try:
        manager = Manager.objects.get(id_manager=id_manager)
    except Manager.DoesNotExist:
        # Gérer le cas où le manager n'existe pas
        raise Http404("Ce manager n'existe pas.")

    if request.method == 'POST':
        # Récupérer les données du formulaire de modification
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_password = request.POST.get('password')

        # Mettre à jour les champs du manager
        manager.username = new_username
        manager.email = new_email
        manager.password = new_password
        manager.save()

        # Rediriger vers une page de confirmation ou une autre vue
        return redirect('admin_home')

    return render(request, 'Admin/list_managers', {'manager': manager})
def supprimer_manager(request,id_manager):
    if request.method == 'GET':
        try:
            manager = Manager.objects.get(id_manager=id_manager)
            manager.delete()
            return redirect('admin_home')
        except Client.DoesNotExist:
            return HttpResponseNotAllowed(['GET'])

    return HttpResponseNotAllowed(['GET'])


def test_view(request):
    return render(request, 'test.html')
def modifier_client(request, numero_client):
    try:
        client = Client.objects.get(numero_client=numero_client)
    except Client.DoesNotExist:
        # Gérer le cas où le manager n'existe pas
        raise Http404("Ce client n'existe pas.")

    if request.method == 'POST':
        # Récupérer les données du formulaire de modification
        new_name = request.POST.get('nom_client')
        new_prenom = request.POST.get('prenom_client')
        new_email = request.POST.get('email_client')


        # Mettre à jour les champs du manager
        client.nom_client = new_name
        client.prenom_client = new_prenom
        client.email_client = new_email
        client.save()

        # Rediriger vers une page de confirmation ou une autre vue
        return redirect('list_clients')

    return render(request, 'Manager/list_clients', {'client': client})

def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        print(password)
        try:
            admin_obj = Admin.objects.get(email=email, password=password)
            # Successful login, store manager ID in session and redirect to manager home page
            request.session['id_admin'] = admin_obj.id_admin
            print(admin_obj.id_admin)

            return redirect('admin_home')
        except Admin.DoesNotExist:
            # Email or password is incorrect, show error message
            messages.error(request, 'Invalid email or password.')

    return render(request, 'Admin/login_admin.html')

def admins_list(request):
    admins = Admin.objects.all()
    return render(request, 'Admin/list_admins.html', {'admins': admins})
def ajouter_admin(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        admin = Admin(username=username, email=email,
                        password=password)
        admin.save()

        return redirect(admins_list)

    return render(request, 'ajouter_client.html')
