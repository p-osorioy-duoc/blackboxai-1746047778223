from django.urls import path
from . import views

app_name = "workshop"

urlpatterns = [
    path("", views.home, name="home"),
    path("owners/", views.owner_list, name="owner_list"),
    path("owners/add/", views.owner_add, name="owner_add"),
    path("vehicles/", views.vehicle_list, name="vehicle_list"),
    path("vehicles/add/", views.vehicle_add, name="vehicle_add"),
    path("vehicles/<int:vehicle_id>/repairs/", views.repair_history, name="repair_history"),
    path("vehicles/<int:vehicle_id>/maintenance/", views.maintenance_schedule, name="maintenance_schedule"),
]
