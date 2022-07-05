from django import forms

from .models import Food,Order

# class for paying money
class PayMoneyForm(forms.Form):
    money = forms.DecimalField(label='繳錢')


# create order
class OrderCreateForm(forms.ModelForm):
    number_of_ordering = forms.DecimalField(label='份量')
    class Meta:
        model = Order
        fields = ['number_of_ordering']


# change food detail (food's name and food's price)
class FoodChangeForm(forms.ModelForm):
    name = forms.CharField(label='餐點')
    price = forms.DecimalField(label='價錢')
    class Meta:
        model = Food
        fields = ['name','price']

# create a food (food's name and food's price)
class FoodCreateForm(forms.ModelForm):
    name = forms.CharField(label='餐點')
    price = forms.DecimalField(label='價錢')
    class Meta:
        model = Food
        fields =['name','price']
    
    def clean_name(self,*args,**kargs):
        name = self.cleaned_data.get('name')
        obj_list = list(Food.objects.all())
        for obj in obj_list:
            if name == obj.name:
                raise forms.ValidationError('這個餐點已經被建立囉')
        return name