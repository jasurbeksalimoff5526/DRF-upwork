from django.contrib import admin

from .models import Bid, Contract, Review


admin.site.register(Bid)
admin.site.register(Contract)
admin.site.register(Review)
