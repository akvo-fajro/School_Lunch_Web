from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Permission
from django.http import Http404

# import self define models and forms
from .models import Food,Order
from .forms import FoodCreateForm,OrderCreateForm,PayMoneyForm,FoodChangeForm

# Create your views here.

# admin

# page of all admin's function
# url : /food/admin/overview
def admin_over_view(request,*args,**kargs):
    if not request.user.is_staff:
        return redirect('/')
    return render(request,'admin_pages/admin_over_view.html',{})

# function to clear all manager
# url : /food/admin/clear_manager
def clear_manager_func(request,*args,**kargs):
    if not request.user.is_staff:
        return redirect('/')
    user_list = list(User.objects.all())
    perm = Permission.objects.get(codename='is_manager')
    for user in user_list:
        if user.has_perm('foods_and_orders.is_manager'):
            user.user_permissions.remove(perm)
    return redirect('/food/admin/overview')

# function to refresh menu
# url : /food/admin/refresh_menu
def refresh_menu_func(request,*args,**kargs):
    if not request.user.is_staff:
        return redirect('/')
    food_list = list(Food.objects.all())
    order_list = list(Order.objects.all())
    for i in range(len(food_list)-1,-1,-1):
        food_list[i].delete()
    for i in range(len(order_list)-1,-1,-1):
        order_list[i].delete()
    return redirect('/food/admin/overview')

# function to clear all user money and manager pay back money
# url : /food/admin/clear_money
def clear_money_func(request,*args,**kargs):
    if not request.user.is_staff:
        return redirect('/')
    user_list = User.objects.all()
    for user in user_list:
        user.useradditionalinformation.money_to_pay = 0
        user.useradditionalinformation.money_pay_back = 0
        user.useradditionalinformation.save()
    return redirect('/food/admin/overview')

# function when order is wrong and need to pay back all the money
# url : /food/admin/order_error
def order_error_func(request,*args,**kargs):
    if not request.user.is_staff:
        return redirect('/')
    user_list = list(User.objects.all())
    for user in user_list:
        order_list = Order.objects.filter(order_sit_number=user.useradditionalinformation.sit_number)
        money_pay_back = 0
        for order in order_list:
            if order.number_of_ordering == 0:
                continue
            order_food = Food.objects.get(food_id=order.food_id)
            money_pay_back += order_food.price*order.number_of_ordering
        for i in range(len(order_list)-1,-1,-1):
            order_list[i].delete()
        if money_pay_back == 0:
            continue
        money_pay_back = money_pay_back
        if user.useradditionalinformation.money_to_pay != 0:
            money_pay_back -= user.useradditionalinformation.money_to_pay
            user.useradditionalinformation.money_to_pay = 0
            user.useradditionalinformation.save()
        user.useradditionalinformation.money_pay_back += money_pay_back
        user.useradditionalinformation.save()
    return redirect('/food/admin/overview')



# manager

# page that list out two hyperlink of manager's view
# url : /food/manager/overview
@login_required(login_url='login')
def manager_over_view(request,*args,**kargs):
    user = User.objects.get(username=request.user)
    if not user.has_perm('foods_and_orders.is_manager'):
        return render(request,'manager_pages/not_manager_view.html',{})
    return render(request,'manager_pages/manager_over_view.html',{})

# function that stop user ordering
# url : /food/manager/stop_order
@login_required(login_url='login')
def stop_order_func(request,*args,**kargs):
    user = User.objects.get(username=request.user)
    if not user.has_perm('foods_and_orders.is_manager'):
        return render(request,'manager_pages/not_manager_view.html',{})
    user_list = User.objects.all()
    for user in user_list:
        if user.has_perm('foods_and_orders.can_order'):
            perm = Permission.objects.get(codename='can_order')
            user.user_permissions.remove(perm)
    return redirect('/food/manager/overview')

# function that start user ordering
# url : /food/manager/start_order
@login_required(login_url='login')
def start_order_func(request,*args,**kargs):
    user = User.objects.get(username=request.user)
    if not user.has_perm('foods_and_orders.is_manager'):
        return render(request,'manager_pages/not_manager_view.html',{})
    user_list = User.objects.all()
    for user in user_list:
        if not user.has_perm('foods_and_orders.can_order'):
            perm = Permission.objects.get(codename='can_order')
            user.user_permissions.add(perm)
    return redirect('/food/manager/overview')

# page that manager use to pay back money
# url : /food/manager/pay_back_money/{{ user_id }}
@login_required(login_url='login')
def pay_back_money_view(request,user_id,*args,**kargs):
    user = User.objects.get(username=request.user)
    if not user.has_perm('foods_and_orders.is_manager'):
        return render(request,'manager_pages/not_manager_view.html',{})
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404("This user isn't exist")
    if user.useradditionalinformation.money_pay_back == 0:
        return redirect('/food/state/money')
    if request.method == 'POST':
        user.useradditionalinformation.money_pay_back = 0
        user.useradditionalinformation.save()
        return redirect('/food/state/money')
    context = {
        'user':user
    }
    return render(request,'manager_pages/pay_back_money_view.html',context)

# function let user get manager's permition
# url : /food/become_manager
@login_required(login_url='login')
def be_manager_functon(request,*args,**kargs):
    user = User.objects.get(username=request.user)
    perm = Permission.objects.get(codename='is_manager')
    user.user_permissions.add(perm)
    return redirect('/food/manager/overview')



# state

# page that list two hyperlink to order and money state
# url : /food/state/overview
@login_required(login_url='login')
def state_over_view(request,*args,**kargs):
    return render(request,'state_pages/state_over_view.html',{})

# page that list out all money paying state
# url : /food/state/money
@login_required(login_url='login')
def money_state_view(request,*args,**kargs):
    nonpay_user_list = []
    money_to_give_user_list = []
    for user in User.objects.all():
        if user.useradditionalinformation.money_to_pay != 0:
            nonpay_user_list.append(user)
        if user.useradditionalinformation.money_pay_back != 0:
            money_to_give_user_list.append(user)
    context = {
        'nonpay_user_list':nonpay_user_list,
        'money_to_give_user_list':money_to_give_user_list
    }
    return render(request,'state_pages/money_state_view.html',context)

# page that list out all order and total money
# url : /food/state/order
@login_required(login_url='login')
def order_state_view(request,*args,**kargs):
    every_food = list(Food.objects.all())
    total_price = 0
    count = 1
    all_list = []
    for food in every_food:
        food_all_order = list(Order.objects.filter(food_id=food.food_id))
        order_number = 0
        for food_order in food_all_order:
            order_number += food_order.number_of_ordering
        if order_number != 0:
            total_price += order_number*food.price
            all_list.append([count,str(food.name),order_number,order_number*food.price])
            count += 1
    context = {
        'all_list':all_list,
        'total_price':total_price
    }
    return render(request,'state_pages/order_state_view.html',context)



# order

# page to order food
# url : /food/order/{{ my_food_id }}
@login_required(login_url='login')
def order_create_view(request,my_food_id,*args,**kargs):
    user = User.objects.get(username=request.user)
    if not user.has_perm('foods_and_orders.can_order'):
        return redirect('/food/cart')
    try:
        my_food = Food.objects.get(food_id = my_food_id)
    except Food.DoesNotExist:
        raise Http404("This food isn't exist")
    try:
        old_order = Order.objects.get(food_id=my_food.food_id,order_sit_number=request.user.useradditionalinformation.sit_number)
        orderform = OrderCreateForm(instance=old_order)
        old_order_number = old_order.number_of_ordering
    except Order.DoesNotExist:
        old_order = False
        orderform = OrderCreateForm()
    if request.method == "POST":
        number_of_order = int(request.POST.get('number_of_ordering'))
        if old_order != False:
            old_money = my_food.price*old_order_number
            old_order.number_of_ordering = number_of_order
            old_order.save()
            my_food.popular = my_food.popular - old_order_number + number_of_order
            my_food.save()
            diff = my_food.price*number_of_order - old_money
            if diff >= 0:
                if user.useradditionalinformation.money_pay_back >= diff:
                    user.useradditionalinformation.money_pay_back -= diff
                else:
                    user.useradditionalinformation.money_to_pay += diff - user.useradditionalinformation.money_pay_back
                    user.useradditionalinformation.money_pay_back = 0
            else:
                if user.useradditionalinformation.money_to_pay >= -diff:
                    user.useradditionalinformation.money_to_pay += diff
                else:
                    user.useradditionalinformation.money_pay_back += -diff - user.useradditionalinformation.money_to_pay
                    user.useradditionalinformation.money_to_pay = 0
            user.useradditionalinformation.save()
            return redirect('/food/menu')
        else:
            new_order = Order(order_sit_number=request.user.useradditionalinformation.sit_number,number_of_ordering=number_of_order,food_id=my_food.food_id)
            new_order.save()
            my_food.popular += number_of_order
            my_food.save()
            user.useradditionalinformation.money_to_pay += my_food.price*number_of_order
            user.useradditionalinformation.save()
            return redirect('/food/menu')
    context={
        'orderform':orderform,
        'my_food':my_food,
    }
    return render(request,'order_pages/order_create_view.html',context)

# page to view the order (cart page)
# url : /food/cart
@login_required(login_url='login')
def cart_view(request,*args,**kargs):
    user_sit_number = request.user.useradditionalinformation.sit_number
    user_order_list = list(Order.objects.filter(order_sit_number=user_sit_number))
    user_order_all_list = []
    total_price = 0
    user_need_to_pay = (request.user.useradditionalinformation.money_to_pay != 0)
    user_order = not (request.user.useradditionalinformation.money_to_pay == request.user.useradditionalinformation.money_pay_back == 0)
    for user_order in user_order_list:
        if user_order.number_of_ordering == 0:
            continue
        user_order_food = Food.objects.get(food_id=user_order.food_id)
        user_order_all_list.append([user_order_food.name,user_order_food.price,user_order.number_of_ordering,user_order_food.price*user_order.number_of_ordering,user_order_food.food_id])
        total_price += user_order_food.price*user_order.number_of_ordering
    context={
        'user_order_all_list':user_order_all_list,
        'total_price':total_price,
        'can_order':User.objects.get(username=request.user).has_perm('foods_and_orders.can_order'),
        'user_need_to_pay':user_need_to_pay,
        'user_order':user_order,
    }
    return render(request,'order_pages/cart_view.html',context)

# page for user to pay money
# url : /food/pay_money
@login_required(login_url='login')
def pay_money_view(request,*args,**kargs):
    user = User.objects.get(username=request.user)
    form = PayMoneyForm()
    if request.method == 'POST':
        money = int(request.POST.get('money'))
        if (user.useradditionalinformation.money_to_pay - money) >= 0:
            user.useradditionalinformation.money_to_pay -= money
            user.useradditionalinformation.save()
        else:
            user.useradditionalinformation.money_pay_back = money - user.useradditionalinformation.money_to_pay
            user.useradditionalinformation.money_to_pay = 0
            user.useradditionalinformation.save()
        return redirect('/food/cart')
    context = {
        'form':form,
        'user':user,
    }
    return render(request,'order_pages/pay_money_view.html',context)



# food

# page to create food
# url : /food/create
@login_required(login_url='login')
def food_create_view(request,*args,**kargs):
    form = FoodCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        food_len = len(list(Food.objects.all()))
        food = Food.objects.get(food_id=0)
        food.food_id = food_len
        food.save()
        form = FoodCreateForm()
    context = {
        'form':form
    }
    return render(request,'food_pages/food_create_view.html',context)

# page to list all the exist food
# url : /food/menu
def food_menu_view(request,*args,**kargs):
    try:
        user = User.objects.get(username=request.user)
        can_order = user.has_perm('foods_and_orders.can_order')
    except User.DoesNotExist:
        can_order = False
    food_list = list(Food.objects.all())
    context = {
        'food_list':food_list,
        'can_order':can_order
    }
    return render(request,'food_pages/food_menu_view.html',context)

# page to change name and price of food
# url : /food/change/{{ my_food_id }}
@login_required(login_url='login')
def food_change_view(request,my_food_id,*args,**kargs):
    try:
        my_food = Food.objects.get(food_id = my_food_id)
    except Food.DoesNotExist:
        raise Http404("This food isn't exist")
    original_price = my_food.price
    form = FoodChangeForm(instance=my_food)
    if request.method == "POST":
        new_name = request.POST.get('name')
        new_price = int(request.POST.get('price'))
        order_list = list(Order.objects.filter(food_id=my_food_id))
        all_user_list = list(User.objects.all())
        for order in order_list:
            for user in all_user_list:
                if user.useradditionalinformation.sit_number != order.order_sit_number:
                    continue
                if new_price > original_price:
                    if user.useradditionalinformation.money_pay_back > (new_price - original_price)*int(order.number_of_ordering):
                        user.useradditionalinformation.money_pay_back -= (new_price - original_price)*int(order.number_of_ordering)
                    else:
                        user.useradditionalinformation.money_to_pay += (new_price - original_price)*int(order.number_of_ordering) - user.useradditionalinformation.money_pay_back
                        user.useradditionalinformation.money_pay_back = 0
                    user.useradditionalinformation.save()
                    break
                elif new_price < original_price:
                    if user.useradditionalinformation.money_to_pay < (original_price - new_price)*int(order.number_of_ordering):
                        user.useradditionalinformation.money_pay_back += (original_price - new_price)*int(order.number_of_ordering) - user.useradditionalinformation.money_to_pay
                        user.useradditionalinformation.money_to_pay = 0
                    else:
                        user.useradditionalinformation.money_to_pay -= (original_price - new_price)*int(order.number_of_ordering)
                    user.useradditionalinformation.save()
                    break
                else:
                    pass
        my_food.name = new_name
        my_food.price = new_price
        my_food.save()
        return redirect('/food/menu')
    context = {
        'form':form
    }
    return render(request,'food_pages/food_change_view.html',context)