from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_recurring_event, name='create_recurring_event'),
]
