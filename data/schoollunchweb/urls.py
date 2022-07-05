from django.contrib import admin
from django.urls import path,include

# import homepage view from accounts_pages
from accounts_pages.views import homepage_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # home page url
    path('',homepage_view,name='home'),

    # accounts pages urls
    path('accounts/',include('accounts_pages.urls')),

    # food pages urls
    path('food/',include('foods_and_orders.urls')),
]
