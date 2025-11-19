from django.contrib import admin

from .models import (
    Buyer,
    Sample,
    Storage,
    SampleBuyerConnection,
    SampleFile,
    StorageFile,
)

admin.site.register(Storage)
admin.site.register(Sample)
admin.site.register(SampleFile)
admin.site.register(Buyer)
admin.site.register(SampleBuyerConnection)
admin.site.register(StorageFile)
