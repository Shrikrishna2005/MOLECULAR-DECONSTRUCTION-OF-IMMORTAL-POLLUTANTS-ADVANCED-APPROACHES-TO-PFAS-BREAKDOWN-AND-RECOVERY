from django.urls import path
from .views import *


urlpatterns = [
    path("pc_login/",pc_login),
    path("pc_reg/",pc_reg),
    path("pc_validate_login/",pc_validate_login),
    path("pc_home/",pc_home),
    path("pc_req/",pc_req),
    path("pc_logout/",pc_logout),
    path("pc_analyze/",pc_analyze),
    path("pc_analyze_process/<int:project_id>/",pc_analyze_process),
    path("pc_report/",pc_report),
]
