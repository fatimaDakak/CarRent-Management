from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls.static import static

from Location import views
from Location.views import reservation_reçus

urlpatterns = [
    # ... existing URL patterns ...

    # Manager login page
    path('manager/login/', views.manager_login, name='manager_login'),
    path('', views.test_view, name='test_view'),
    # Manager home page
    path('manager/home/', views.manager_home, name='manager_home'),
    path('reservation_reçus/', reservation_reçus, name='reservation_reçus'),
    path('logout/', views.logout_view, name='logout'),
    path('list_clients/', views.list_clients, name='list_clients'),
    path('ajouter_client/', views.ajouter_client, name='ajouter_client'),
    path('clients/<int:numero_client>/', views.supprimer_client, name='supprimer_client'),
    path('make_reservation/', views.make_reservation, name='make_reservation'),
    path('admin/home',views.admin_home,name='admin_home'),
    path('managers/<int:id_manager>/modifier/', views.modifier_manager, name='modifier_manager'),
path('clients/<int:numero_client>/modifier/', views.modifier_client, name='modifier_client'),
    path('managers/<int:id_manager>/', views.supprimer_manager, name='supprimer_manager'),
        path('test_view/', views.test_view, name='test_view'),
    path('liste-managers/', views.liste_managers, name='liste-managers'),
    path('modifier-manager/<str:username>/', views.modifier_manager, name='modifier-manager'),

                  path('admin/login/', views.admin_login, name='admin_login'),
                  path('list_admins', views.admins_list, name='admins_list'),
                  path('admin/ajouter', views.ajouter_admin, name='ajouter_admin'),

              ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
