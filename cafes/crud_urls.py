from django.urls import path
from .views import (
    RecordListView,
    RecordCreateView,
    RecordUpdateView,
    RecordDeleteView, update_drafts,
)

urlpatterns = [
    path("", RecordListView.as_view(), name="crud_list"),  # Список ресторанов
    path("create/", RecordCreateView.as_view(), name="crud_create"),  # Создание ресторана
    path("<int:pk>/update/", RecordUpdateView.as_view(), name="crud_update"),  # Обновление ресторана
    path("<int:pk>/delete/", RecordDeleteView.as_view(), name="crud_delete"),  # Удаление ресторана
    path("update-drafts/", update_drafts, name="update_drafts"),
]
