from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from core import models


@receiver(post_save, sender=models.State, dispatch_uid='create_file')
def create_file(**kwargs):
    instance = kwargs.get('instance')
    with open(f"{instance.id}.txt", "w+") as file:
        file.write(f'{instance.name} | {instance.abbreviation}')


@receiver(pre_save, sender=models.SaleItem, dispatch_uid='persist_sale_price')
def persist_sale_price(**kwargs):
    instance: models.SaleItem = kwargs.get('instance')
    instance.sale_price = instance.product.sale_price
