from django.contrib import admin
from .models import Room, Message

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug']
#     prepopulated_fields = {'slug': ('name',)}

admin.site.register(Room)

# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug', 'price', 'stock',
#                     'available', 'created', 'updated']
#     list_filter = ['available', 'created', 'updated']
#     list_editable = ['price', 'stock', 'available']
#     prepopulated_fields = {'slug': ('name',)}

admin.site.register(Message)
