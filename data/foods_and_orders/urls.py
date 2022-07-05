from django.urls import path

from .views import *

urlpatterns = [
    # food
    path('create',food_create_view,name='food_create'),
    path('menu',food_menu_view,name='food_menu'),
    path('change/<int:my_food_id>',food_change_view,name='food_change'),

    # order
    path('order/<int:my_food_id>',order_create_view,name='order_create'),
    path('cart',cart_view,name='cart'),
    path('pay_money',pay_money_view,name='pay_money'),

    # state
    path('state/overview',state_over_view,name='state_overview'),
    path('state/money',money_state_view,name='money_state'),
    path('state/order',order_state_view,name='order_state'),

    # manager
    path('manager/overview',manager_over_view,name='manager_overview'),
    path('manager/stop_order',stop_order_func,name='stop_order'),
    path('manager/start_order',start_order_func,name='start_order'),
    path('manager/pay_back_money/<int:user_id>',pay_back_money_view,name='pay_back_money'),
    path('become_manager',be_manager_functon,name='become_manager'),

    # admin
    path('admin/overview',admin_over_view,name='admin_overview'),
    path('admin/clear_manager',clear_manager_func,name='clear_manager'),
    path('admin/refresh_menu',refresh_menu_func,name='refresh_menu'),
    path('admin/clear_money',clear_money_func,name='clear_money'),
    path('admin/order_error',order_error_func,name='order_error'),
]