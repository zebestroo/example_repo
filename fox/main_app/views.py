from django.shortcuts import render
from django.conf import settings
from django.http.response import JsonResponse
from .models import Item, Order, Tax, Discount
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


def order_list(request):
    item_ids = request.POST.getlist('items')
    if item_ids:
        names = [Item.objects.get(id=item_id).name for item_id in item_ids]
        scale = sum([Item.objects.get(id=item_id).price for item_id in item_ids])

        # Select first tax for example
        if Tax.objects.all():
            taxes = [Tax.objects.all()[0].id]
        else:
            taxes = []

        # Select first discount for example
        if Discount.objects.all():
            discounts = [discount_dict(Discount.objects.all()[0])]
        else:
            discounts = []

        new_order = Order(
            data_json={
                'item_ids': item_ids,
                'taxes': taxes,
                'discounts': discounts,
            },
            total_scale=scale,
        )
        new_order.save()
        data = {'order_data': new_order, 'names': names}
        return render(request, 'main_app/order_list.html', data)
    else:
        data = {'items': Item.objects.all()}
        return render(request, 'main_app/index.html', data)


def order(request, order_id):
    data = {'order': Order.objects.get(id=order_id)}
    return render(request, 'main_app/order.html', data)


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


def buy_order(request, order_id):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            order_object = Order.objects.get(id=order_id)
            item_ids = order_object.data_json['item_ids']
            discounts = order_object.data_json['discounts']
            taxes = order_object.data_json['taxes']

            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success/',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[line_item(item_id, taxes) for item_id in item_ids],
                discounts=discounts,
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


def create_tax(percentage=0, inclusive=False, name='Empty name'):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    tax = stripe.TaxRate.create(percentage=percentage, display_name=name, inclusive=inclusive)
    Tax.objects.create(id=tax.id, percentage=tax.percentage, inclusive=tax.inclusive)


def create_discount(discount_type='coupon', amount_off=None, percent_off=None):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if discount_type == 'coupon':
        if amount_off:
            coupon = stripe.Coupon.create(amount_off=amount_off)
        if percent_off:
            coupon = stripe.Coupon.create(percent_off=percent_off)
        Discount.objects.create(type=discount_type, id=coupon.id)


def line_item(price_id, tax_rate_ids=[]):
    return {
                'price': price_id,
                'quantity': 1,
                'tax_rates': tax_rate_ids,
            }


def discount_dict(discount):
    return {discount.type: discount.id}
