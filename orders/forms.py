from django import forms

from .models import Orders

LABEL_FORM_CONTROL = 'form-control'
LABEL_ATTR_CLASS = 'class'
LABEL_ATTR_PLACEHOLDER = 'placeholder'


class OrdersForm(forms.ModelForm):

    """Описывает форму оформления заказа.

   OrdersForm является формой, связанной с моделью. Модель - Orders.
   Атрибуты(поля формы):
       1. first_name - имя получателя заказа. Получателем не обязательно должен быть человек, который
          оформляет заказ
       2. last_name - фамилия получателя заказа
       3. email - адрес электронной почты для связи
       4. address - адрес доставки

    """
    first_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.widgets.TextInput(
            attrs={
                LABEL_ATTR_CLASS: LABEL_FORM_CONTROL,
                LABEL_ATTR_PLACEHOLDER: 'Иван',
            }
        )
    )
    last_name = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.widgets.TextInput(
            attrs={
                LABEL_ATTR_CLASS: LABEL_FORM_CONTROL,
                LABEL_ATTR_PLACEHOLDER: 'Иванов',
            }
        )
    )
    email = forms.EmailField(
        required=True,
        max_length=50,
        widget=forms.widgets.EmailInput(
            attrs={
                LABEL_ATTR_CLASS: LABEL_FORM_CONTROL,
                LABEL_ATTR_PLACEHOLDER: 'you@example.com',
            }
        )
    )
    address = forms.CharField(
        required=True,
        max_length=500,
        widget=forms.widgets.TextInput(
            attrs={
                LABEL_ATTR_CLASS: LABEL_FORM_CONTROL,
                LABEL_ATTR_PLACEHOLDER: 'Россия, Москва, ул. Мира, дом 6',
            }
        )
    )

    class Meta:
        model = Orders
        fields = (
            'first_name',
            'last_name',
            'email',
            'address',
        )
