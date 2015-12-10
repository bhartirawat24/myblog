from django.contrib import admin
from blogapp.models import Profile,BlogTable,Category

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
	fields = ['user','contact','activationkey', 'gender','image']

admin.site.register(Profile,ProfileAdmin)

class BlogTableAdmin(admin.ModelAdmin):
	fields =['user','title','description','status']

admin.site.register(BlogTable,BlogTableAdmin)

class CategoryAdmin(admin.ModelAdmin):
	fields =['name','status']

admin.site.register(Category,CategoryAdmin)
