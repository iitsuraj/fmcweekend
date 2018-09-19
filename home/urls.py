from django.urls import path
from . import views

urlpatterns = [
    path('',views.landing,name="landing"),
    path('register/',views.register,name="register"),
    # path('team/',views.team,name="team"),
    path('gallery/',views.gallery,name="gallery"),
    path('events/',views.events,name="events"),
    path('checkout/',views.paymentConfirmationView,name="checkout"),
    path('thanks/',views.freeCheckoutView,name="free_checkout"),
    path('index/',views.index,name="index"),
    # path('ca/',views.CaView,name="ca"),
    # path('registration/',views.RegistrationView,name="regview"),
]

