from django.urls import path
from .views import ListVunerabilitiesView,RetrieveUpdateVunerabilitiesView

urlpatterns = [
    path('reports/',ListVunerabilitiesView.as_view()),
    path('reports/<int:report_id>/', RetrieveUpdateVunerabilitiesView.as_view())
]