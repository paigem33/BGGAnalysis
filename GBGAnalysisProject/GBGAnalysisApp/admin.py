from django.contrib import admin
from .models import GameBoard
from .models import Review


# Register your models here.

admin.site.register(GameBoard)
admin.site.register(Review)