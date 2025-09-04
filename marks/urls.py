
from django.urls import path
from .views import dashboard, export_excel, export_pdf

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("export_excel/", export_excel, name="export_excel"),
    path("export_pdf/", export_pdf, name="export_pdf"),
]
