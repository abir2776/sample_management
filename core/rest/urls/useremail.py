from django.urls import path

from core.rest.views.useremail import ContactFormAPIView

urlpatterns = [
    path("", ContactFormAPIView.as_view(), name="contact-form"),
]
