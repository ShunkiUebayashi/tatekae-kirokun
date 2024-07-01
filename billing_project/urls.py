from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("billing.urls")),  # accounts/ のパスを追加
    path("billing/", include("billing.urls")),  # billing/ のパスを追加
    path("", include("billing.urls")),  # これで /login も対応可能に
]
