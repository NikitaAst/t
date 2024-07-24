from django.urls import path
from .views import AdvertListView

urlpatterns = [
    path('adverts/', AdvertListView.as_view(), name='advert-list'),
]