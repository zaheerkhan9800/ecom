import datetime
import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .serializers import UserSerailizer

from .forms import CreateUserForm
# Create your views here.
from .models import *
from .utils import cartData, guestOrder


def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)



from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)


                template = render_to_string('store/email_template.html', {'name': form.cleaned_data.get('username')})

                email = EmailMessage(
                    "Thanks for signing up! Keep learning",
                    template,
                    settings.EMAIL_HOST_USER,
                    [form.cleaned_data.get('email')],

                )

                email.fail_silently = False,
                email.send()



                #subject, from_email, to = 'Hello form.cleaned_data.get("username")', 'settings.EMAIL_HOST_USER', 'form.cleaned_data.get("email")'

                '''text_content = 'Hey,Thanks For Signing Up with us'
                html_content = '<p>This is an <strong>important</strong> message.</p>'
                msg = EmailMultiAlternatives(text_content,html_content, settings.EMAIL_HOST_USER, [form.cleaned_data.get('email')])
                msg.attach_alternative(html_content, "text/html")
                msg.attach_file('static/images/shoes.jpg')
                msg.send()'''

                return redirect('login')

        context = {'form': form}
        return render(request, 'store/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('store')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, "store/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect('login')





def userSettings(request):
    user, created = User.objects.get_or_create(id=1)

    setting = user.setting
    seralizer = UserSerailizer(setting, many=False)

    return JsonResponse(seralizer.data, safe=False)


def updateTheme(request):
    data = json.loads(request.body)
    theme = data['theme']

    user, created = User.objects.get_or_create(id=1)
    user.setting.value = theme
    user.setting.save()
    print('Request:', theme)
    return JsonResponse('Updated..', safe=False)


def aboutus(request):
    return render(request, 'store/about.html')



def contactus(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()

    return render(request, 'store/contactus.html')


def slider(request, id):
    product = Product.objects.get(id=id)

    context = {'product': product}
    return render(request, 'store/productView.html', context)
