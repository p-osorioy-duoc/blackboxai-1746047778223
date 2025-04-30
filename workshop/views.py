from django.shortcuts import render, get_object_or_404, redirect
from .models import Owner, Vehicle, RepairHistory, MaintenanceSchedule
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse

def home(request):
    return render(request, "workshop/home.html")

def owner_list(request):
    query = request.GET.get("q")
    owners = Owner.objects.all()
    if query:
        owners = owners.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )
    return render(request, "workshop/owner_list.html", {"owners": owners, "query": query})

def owner_add(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        Owner.objects.create(first_name=first_name, last_name=last_name, email=email, phone=phone)
        return redirect("workshop:owner_list")
    return render(request, "workshop/owner_add.html")

def vehicle_list(request):
    query = request.GET.get("q")
    vehicles = Vehicle.objects.select_related("owner").all()
    if query:
        vehicles = vehicles.filter(
            Q(make__icontains=query) |
            Q(model__icontains=query) |
            Q(license_plate__icontains=query) |
            Q(owner__first_name__icontains=query) |
            Q(owner__last_name__icontains=query)
        )
    return render(request, "workshop/vehicle_list.html", {"vehicles": vehicles, "query": query})

def vehicle_add(request):
    owners = Owner.objects.all()
    if request.method == "POST":
        owner_id = request.POST.get("owner")
        make = request.POST.get("make")
        model = request.POST.get("model")
        year = request.POST.get("year")
        license_plate = request.POST.get("license_plate")
        owner = get_object_or_404(Owner, id=owner_id)
        Vehicle.objects.create(owner=owner, make=make, model=model, year=year, license_plate=license_plate)
        return redirect("workshop:vehicle_list")
    return render(request, "workshop/vehicle_add.html", {"owners": owners})

def repair_history(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == "POST":
        description = request.POST.get("description")
        date = request.POST.get("date")
        RepairHistory.objects.create(vehicle=vehicle, description=description, date=date)
        return HttpResponseRedirect(reverse("workshop:repair_history", args=[vehicle_id]))
    repairs = vehicle.repair_histories.order_by("-date")
    return render(request, "workshop/repair_history.html", {"vehicle": vehicle, "repairs": repairs})

def maintenance_schedule(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == "POST":
        maintenance_type = request.POST.get("maintenance_type")
        scheduled_date = request.POST.get("scheduled_date")
        MaintenanceSchedule.objects.create(vehicle=vehicle, maintenance_type=maintenance_type, scheduled_date=scheduled_date)
        return HttpResponseRedirect(reverse("workshop:maintenance_schedule", args=[vehicle_id]))
    schedules = vehicle.maintenance_schedules.order_by("scheduled_date")
    today = timezone.now().date()
    past_maintenances = schedules.filter(scheduled_date__lt=today)
    upcoming_maintenances = schedules.filter(scheduled_date__gte=today)
    return render(request, "workshop/maintenance_schedule.html", {
        "vehicle": vehicle,
        "past_maintenances": past_maintenances,
        "upcoming_maintenances": upcoming_maintenances,
    })
