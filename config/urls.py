"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import urls
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404, handler403
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("pages.urls")),
    path("",include("accounts.urls")),
    path("products/",include("products.urls")),
    path("cart/",include("cart.urls")),
    path("orders/",include("orders.urls")),
    path("checkout/",include("payments.urls")), 
]


# config to server images
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# config customs errors pages.
def custom_404_view(request, exception):
    return render(request, 'errors/404.html', status=404)

def custom_403_view(request, exception):
    return render(request, 'errors/403.html', status=403)

handler404 = custom_404_view
handler403 = custom_403_view