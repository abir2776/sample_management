from django.contrib import admin

from .models import Buyer, Sample, Bucket, SampleBuyerConnection, SampleFile

admin.site.register(Bucket)
admin.site.register(Sample)
admin.site.register(SampleFile)
admin.site.register(Buyer)
admin.site.register(SampleBuyerConnection)
