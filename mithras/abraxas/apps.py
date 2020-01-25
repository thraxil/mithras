from django.apps import AppConfig
from django.conf import settings
import beeline


class AbraxasConfig(AppConfig):
    name = 'mithras.abraxas'

    def ready(self):
        if settings.HONEYCOMB_WRITEKEY and settings.HONEYCOMB_DATASET:
            beeline.init(
                writekey=settings.HONEYCOMB_WRITEKEY,
                dataset=settings.HONEYCOMB_DATASET,
                service_name='abraxas'
            )
