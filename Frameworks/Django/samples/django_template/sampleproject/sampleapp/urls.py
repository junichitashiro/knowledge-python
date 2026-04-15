from django.urls import path

from sampleapp import views

urlpatterns = [
    path('new/', views.sample_new, name='sample_new'),
    path('<int:sample_id>/', views.sample_detail, name='sample_detail'),
    path('<int:sample_id>/edit/', views.sample_edit, name='sample_edit'),
]
