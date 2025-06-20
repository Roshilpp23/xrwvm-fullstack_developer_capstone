from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views  # ✅ Import views

app_name = 'djangoapp'

urlpatterns = [
    # ✅ User Authentication
    path('register', view=views.registration, name='register'),
    path('login', view=views.login_user, name='login'),
    path('logout', view=views.logout_request, name='logout'),

    # ✅ Car Models
    path('get_cars', view=views.get_cars, name='getcars'),

    # ✅ Dealerships
    path('get_dealers', view=views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),

    # ✅ Dealer Details
    path('dealer/<int:dealer_id>', view=views.get_dealer_details, name='dealer_details'),

    # ✅ Dealer Reviews with Sentiment
    path('reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_reviews'),

    # ✅ Add Review
    path('add_review', view=views.add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
