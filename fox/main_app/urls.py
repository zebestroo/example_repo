from django.urls import path
from .views import *


urlpatterns = [
    path('', main_page, name='home'),
    path('item/<slug:item_id>', item, name='item'),
    path('buy/<slug:item_id>', buy, name='buy'),
    path('conf/', stripe_conf, name='stripe_conf'),
    path('success/', success_way_page, name='success_way_page'),
    path('cancelled/', bad_way_page, name='bad_way_page')
]
