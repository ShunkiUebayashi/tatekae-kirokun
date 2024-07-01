from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.invoice_list, name="invoice_list"),
    path("create/", views.create_invoice, name="create_invoice"),
    path("approve/<int:pk>/", views.approve_invoice, name="approve_invoice"),
    path("register/", views.register, name="register"),
    path("password_reset/", views.password_reset, name="password_reset"),
    path("password_reset_secret/", views.password_reset_secret, name="password_reset_secret"),
    path("logout/", views.logout_view, name="logout"),
    path("password_change/", views.password_change, name="password_change"),
    path("password_change/done/", views.password_change_done, name="password_change_done"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("sent_pending_invoices/", views.sent_pending_invoices, name="sent_pending_invoices"),
    path("sent_approved_invoices/", views.sent_approved_invoices, name="sent_approved_invoices"),
    path("received_pending_invoices/", views.received_pending_invoices, name="received_pending_invoices"),
    path("received_approved_invoices/", views.received_approved_invoices, name="received_approved_invoices"),
]
