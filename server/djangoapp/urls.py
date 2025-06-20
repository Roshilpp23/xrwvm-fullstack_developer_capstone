from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views  # ✅ Import views

app_name = 'djangoapp'

urlpatterns = [
    # ✅ Path for user registration
    path(route='register', view=views.registration, name='register'),

    # ✅ Path for user login
    path('login', view=views.login_user, name='login'),

    # ✅ Path for user logout
    path('logout', view=views.logout_request, name='logout'),

    # ✅ Path to get cars
    path('get_cars', view=views.get_cars, name='getcars'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
