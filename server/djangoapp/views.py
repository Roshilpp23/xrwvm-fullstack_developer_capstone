from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

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
    if request.method == "GET":  # React frontend uses GET for logout
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

            # Create and log in the new user
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
