from django.urls import path

from shop.watch_shop.views import home_view, CatalogueView, WatchDetail, add_to_cart, remove_single_item_from_cart, \
    remove_from_cart, CheckoutView, OrderSummaryView

urlpatterns = [
    path('', home_view, name="home"),
    path('browse/', CatalogueView.as_view(), name="browse"),
    path('detail/<slug>/', WatchDetail.as_view(), name='detail'),
    path('add-to-cart/<slug>/', add_to_cart, name='add to cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove from cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove single item from cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
