# api/views.py
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Train, Booking
from django.db import transaction
from django.db.models import F

from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        "signup": "/api/signup/",
        "login": "/api/login/",
        "trains_create": "/api/trains/create/",
        "trains_availability": "/api/trains/availability/",
        "book_seat": "/api/trains/<train_id>/book/",
    })
@api_view(['POST'])
def signup(request):
    data = request.data
    user = User.objects.create_user(
        username=data['username'], password=data['password'], email=data['email']
    )
    return Response({"status": "Account successfully created", "user_id": user.id})

@api_view(['POST'])
def login(request):
    data = request.data
    user = User.objects.filter(username=data['username']).first()
    if user and user.check_password(data['password']):
        refresh = RefreshToken.for_user(user)
        return Response({
            "status": "Login successful",
            "user_id": user.id,
            "access_token": str(refresh.access_token)
        })
    return Response({"status": "Incorrect username/password"}, status=401)

@api_view(['POST'])
def add_train(request):
    data = request.data
    train = Train.objects.create(
        name=data['train_name'],
        source=data['source'],
        destination=data['destination'],
        seat_capacity=data['seat_capacity'],
        available_seats=data['seat_capacity'],
        arrival_time_at_source=data['arrival_time_at_source'],
        arrival_time_at_destination=data['arrival_time_at_destination'],
    )
    return Response({"message": "Train added successfully", "train_id": train.id})

@api_view(['GET'])
def check_availability(request):
    source = request.query_params.get('source')
    destination = request.query_params.get('destination')
    trains = Train.objects.filter(source=source, destination=destination)
    availability = [
        {"train_id": train.id, "train_name": train.name, "available_seats": train.available_seats}
        for train in trains
    ]
    return Response(availability)

@api_view(['POST'])
def book_seat(request, train_id):
    data = request.data
    user_id = data['user_id']
    no_of_seats = data['no_of_seats']
    
    with transaction.atomic():
        train = Train.objects.select_for_update().get(id=train_id)
        if train.available_seats >= no_of_seats:
            train.available_seats = F('available_seats') - no_of_seats
            train.save()
            booking = Booking.objects.create(user_id=user_id, train=train, seats_booked=no_of_seats)
            return Response({
                "message": "Seat booked successfully",
                "booking_id": booking.id,
                "seat_numbers": list(range(1, no_of_seats + 1))
            })
        else:
            return Response({"error": "Not enough seats available"}, status=400)
