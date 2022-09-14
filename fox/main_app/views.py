from django.shortcuts import render
from django.conf import settings
from django.http.response import JsonResponse
from .models import Item
import stripe

# Create your views here.


def main_page(request):
    if request.method == 'POST':
        create_product(request)
    data = {'items': Item.objects.all()}
    return render(request, 'main_app/index.html', data)


def item(request, item_id):
    data = {'item': Item.objects.get(id=item_id)}
    return render(request, 'main_app/item.html', data)


def buy(request, item_id):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success/',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                                 {
                                     'price': item_id,
                                     'quantity': 1,
                                 },
                             ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


def stripe_conf(request):
    if request.method == "GET":
        stripe_config = {'public_key': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


def success_way_page(request):
    return render(request, 'main_app/success.html')


def bad_way_page(request):
    return render(request, 'main_app/fail.html')


def create_product(request):
    name = request.POST.get('name')
    description = request.POST.get('description')
    price = int(request.POST.get('price'))
    stripe.api_key = settings.STRIPE_SECRET_KEY
    product = stripe.Product.create(stripe.api_key, name=name, description=description)
    default_price = stripe.Price.create(stripe.api_key, currency='usd', unit_amount=price, product=product)
    product.modify(product.id, default_price=default_price)
    Item.objects.create(name=name, description=description, price=price/100, id=default_price.id)