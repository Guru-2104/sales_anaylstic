from django.contrib import admin
from django.urls import path

from sales.views import (
    login_view,
    logout_view,
    upload_csv,
    dashboard
)


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        login_view,
        name="home"
    ),

    path(
        "login/",
        login_view,
        name="login"
    ),

    path(
        "logout/",
        logout_view,
        name="logout"
    ),

    path(
        "upload/",
        upload_csv,
        name="upload_csv"
    ),

    path(
        "dashboard/",
        dashboard,
        name="dashboard"
    ),

]