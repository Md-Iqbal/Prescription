from django.contrib import admin
from . models import Post, Profile, T_View, Following

admin.site.register(Post)
admin.site.register(T_View)
admin.site.register(Profile)
admin.site.register(Following)
