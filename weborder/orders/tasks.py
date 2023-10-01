from celery import shared_task
from .models import Order
import time

@shared_task
def process_order(order_id):
    order = Order.objects.get(id=order_id)
    time.sleep(10)  # имитация обработки заказа
    order.status = 'completed'
    order.save()
