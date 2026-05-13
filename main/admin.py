from django.contrib import admin
from .models import Article, Blog, Content, Profile, HireRequest, Chat, Message
from .models import HireRequest

admin.site.register(Article)
admin.site.register(Blog)
admin.site.register(Content)
admin.site.register(Profile)
admin.site.register(HireRequest)
admin.site.register(Chat)
admin.site.register(Message)
