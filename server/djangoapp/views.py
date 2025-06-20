from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# ✅ Import Car Models and the initiate function
from .models import CarMake, CarModel
from .populate import initiate

# ✅ Import backend proxy utilities
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)

# ✅ LOGIN VIEW
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("userName")
            password = data.get("password")

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                logger.info(f"Login successful for user: {username}")
                return JsonResponse({"userName": username, "status": "Authenticated"}, status=200)
            else:
                logger.warning(f"Login failed for user: {username}")
                return JsonResponse({"message": "Invalid credentials"}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)

    return JsonResponse({"message": "Invalid request method"}, status=400)

# ✅ LOGOUT VIEW
@csrf_exempt
def logout_request(request):
    if request.method == "GET":
        logout(request)
        logger.info("User logged out successfully.")
        return JsonResponse({"userName": ""}, status=200)
    return JsonResponse({"message": "Invalid request method"}, status=400)

# ✅ REGISTRATION VIEW
@csrf_exempt
def registration(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("userName")
            password = data.get("password")
            first_name = data.get("firstName")
            last_name = data.get("lastName")
            email = data.get("email")

            if User.objects.filter(username=username).exists():
                logger.warning(f"Registration attempt for existing user: {username}")
                return JsonResponse({"error": "Already Registered"}, status=400)

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            login(request, user)
            logger.info(f"User registered and logged in: {username}")
            return JsonResponse({"userName": username, "status": "Registered & Authenticated"}, status=200)

        except Exception as e:
            logger.error(f"Error during registration: {str(e)}")
            return JsonResponse({"message": "Registration failed"}, status=500)

    return JsonResponse({"message": "Invalid request method"}, status=400)

# ✅ GET CARS VIEW
@csrf_exempt
def get_cars(request):
    count = CarMake.objects.filter().count()
    print("CarMake count:", count)
    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })

    return JsonResponse({"CarModels": cars})

# ✅ GET DEALERSHIPS (ALL or BY STATE)
@csrf_exempt
def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})

# ✅ GET A SINGLE DEALER BY ID
@csrf_exempt
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealer = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealer})
    return JsonResponse({"status": 400, "message": "Bad Request"})

# ✅ GET REVIEWS FOR A DEALER WITH SENTIMENTS
@csrf_exempt
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            sentiment = analyze_review_sentiments(review_detail.get('review', ''))
            review_detail['sentiment'] = sentiment
        return JsonResponse({"status": 200, "reviews": reviews})
    return JsonResponse({"status": 400, "message": "Bad Request"})

# ✅ ADD REVIEW (POST)
@csrf_exempt
def add_review(request):
    if request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            response = post_review(data)
            if response:
                return JsonResponse({"status": 200, "message": "Review posted successfully"})
            else:
                return JsonResponse({"status": 500, "message": "Failed to post review"})
        except Exception as e:
            print("Error posting review:", e)
            return JsonResponse({"status": 400, "message": "Bad Request"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
