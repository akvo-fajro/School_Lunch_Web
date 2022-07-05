from django.contrib.auth.models import User,Permission
from foods_and_orders.models import Food,Order

# this function will clear all users' money , manager , food , and order
# Also open the permission let user order
def new_day():
    user_list = list(User.objects.all())
    perm = Permission.objects.get(codename='is_manager')
    perm_order = Permission.objects.get(codename='can_order')
    for user in user_list:
        user.useradditionalinformation.money_to_pay = 0
        user.useradditionalinformation.money_pay_back = 0
        user.useradditionalinformation.save()
        if user.has_perm('foods_and_orders.is_manager'):
            user.user_permissions.remove(perm)
        if not user.has_perm('foods_and_orders.can_order'):
            user.user_permissions.add(perm_order)
    food_list = list(Food.objects.all())
    order_list = list(Order.objects.all())
    for i in range(len(food_list)-1,-1,-1):
        food_list[i].delete()
    for i in range(len(order_list)-1,-1,-1):
        order_list[i].delete()

new_day()