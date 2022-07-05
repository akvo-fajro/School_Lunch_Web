from django.contrib.auth.models import User,Permission

# this function will take off the permission of user to order
def stop_ordering():
    user_list = User.objects.all()
    for user in user_list:
        if user.has_perm('foods_and_orders.can_order'):
            perm = Permission.objects.get(codename='can_order')
            user.user_permissions.remove(perm)

stop_ordering()