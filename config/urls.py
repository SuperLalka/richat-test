
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView

from app.items import views as items_views
from app.users import views as users_views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('buy/success/', TemplateView.as_view(template_name="stripe/success.html")),
    path('buy/cancel/', TemplateView.as_view(template_name="stripe/cancel.html")),
    path('buy/', items_views.buy),

    path('item/<int:item_id>/', items_views.ItemDetailPageView.as_view(), name='item_page'),
    path('items/', items_views.ItemListPageView.as_view(), name='items_page'),
    path('basket/', users_views.BasketPageView.as_view(), name='basket_page'),
    path('basket/operation/<int:item_id>/', users_views.operation),
    path('orders/', items_views.OrdersListPageView.as_view(), name='orders_page'),

    path('webhooks/', items_views.webhooks),

    re_path('', items_views.HomePageView.as_view(), name='home_page'),
]
