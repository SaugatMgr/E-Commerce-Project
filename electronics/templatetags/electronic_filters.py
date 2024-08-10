from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()


@register.filter
def get_todays_deals_products(products):
    time_limit = timezone.now() - timedelta(hours=24)

    return products.filter(added_date__gte=time_limit, is_today_deal=True)
