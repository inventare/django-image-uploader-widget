from django.urls import path
from . import views

urlpatterns = [
    path("required/", views.widget_required, name='required'),
    path("required/<pk>/", views.widget_required),
    path("optional/", views.widget_optional, name='optional'),
    path("optional/<pk>/", views.widget_optional),
    path("array_field/", views.array_field_required, name='array'),
    path("array_field/<pk>/", views.array_field_required),
    path("base/", views.base),
    path("base/light/", views.base_light),
    path("base/dark/", views.base_dark),
]
