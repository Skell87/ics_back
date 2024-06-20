"""
URL configuration for ics_back_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from  rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from ics_back_app.views import (
    get_profile,
    register_user,
    inventory_detail_list,
    add_warehouse_section,
    add_warehouse_sub_section,
    add_warehouse_sub_sub_section,
    delete_inventory_item,
    delete_warehouse_section,
    delete_warehouse_sub_section,
    delete_warehouse_sub_sub_section,
    update_inventory_item
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', get_profile),
    path('refresh/', TokenRefreshView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('register_user/', register_user),
    path('inventory_detail_list/', inventory_detail_list),
    path('add_warehouse_section/', add_warehouse_section),
    path('delete_warehouse_section/<int:section_id>/', delete_warehouse_section),
    path('add_warehouse_sub_section/', add_warehouse_sub_section),
    path('delete_warehouse_sub_section/<int:sub_section_id>/', delete_warehouse_sub_section),
    path('add_warehouse_sub_sub_section/', add_warehouse_sub_sub_section),
    path('delete_warehouse_sub_sub_section/<int:sub_sub_section_id>/', delete_warehouse_sub_sub_section),
    path('delete_inventory_item/<int:pk>/', delete_inventory_item),
    path('update_inventory_item/<int:pk>/', update_inventory_item)
    # path('get_inventory_details/', get_inventory_details)
]

