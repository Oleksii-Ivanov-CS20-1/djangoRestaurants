from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import add_review, RecordListView, RecordCreateView, RecordUpdateView, RecordDeleteView
from allauth.account.views import LoginView

urlpatterns = [
    path("", views.RestaurantView.as_view()),
    path("accounts/", include("allauth.urls")),
    path("login/", LoginView.as_view(template_name="cafes/login.html"), name="login"),  # Вход
    path("logout/", views.logout_view, name="logout"),  # Выход
    path("register/", views.register, name="register"),  # Регистрация
    path("admin-panel/", views.admin_panel_redirect, name="admin_panel"),

    path("filter/", views.FilterCafesView.as_view(), name="filter"),
    path("search/", views.Search.as_view(), name="search"),
    path("add-rating/", views.AddStarRating.as_view(), name="add_rating"),
    path("<slug:slug>/", views.RestaurantDetailView.as_view(), name="restaurants_detail"),
    path('add_review/<int:restaurant_id>/', add_review, name='add_review'),
]

