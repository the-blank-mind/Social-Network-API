from django.contrib import admin
from .models import User,FriendRequest
# Register your models here.


@admin.register(User)
class userregister(admin.ModelAdmin):
    list_display= ['id','email']