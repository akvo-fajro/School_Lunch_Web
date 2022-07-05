from foods_and_orders.models import Order
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
content_type = ContentType.objects.get_for_model(Order)
permission1 = Permission.objects.create(codename='is_manager',name='is manager',content_type=content_type)
permission2 = Permission.objects.create(codename='can_order',name='can order',content_type=content_type)