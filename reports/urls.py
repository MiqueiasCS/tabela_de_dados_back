from django.urls import path
from .views import ReportsView

urlpatterns = [
    path('reports/',ReportsView.as_view()),
    path('reports/<int:report_id>/', ReportsView.as_view())
]