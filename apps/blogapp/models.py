from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	GENDER_STATUS = ((0,'Female'),(1,'Male'))
	user = models.OneToOneField(User,unique=True, related_name='profile')
	contact = models.CharField(max_length=100,blank=True,default='',unique=True)
	activationkey = models.CharField(max_length=232,blank=True,null=True)
	gender = models.SmallIntegerField(choices=GENDER_STATUS,default=0)
	image = models.ImageField(upload_to='profile_image',blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

class Category(models.Model):
	STATUS_CHOICE = ((0,'Inactive'),(1,'active'),(2,'Delete'))
	name = models.CharField(max_length=100)
	status = models.SmallIntegerField(choices=STATUS_CHOICE)
	created_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

class BlogTable(models.Model):
	STATUS_CHOICE = ((0,'Inactive'),(1,'active'),(2,'Delete'))
	PUBLISH_CHOICE = ((0,'False'),(1,'True'))
	user = models.ForeignKey(User)
	title = models.CharField(max_length=100)
	description = models.TextField(max_length=500,blank=True,null=True)
	status = models.SmallIntegerField(choices=STATUS_CHOICE)
	is_publish = models.SmallIntegerField(choices=PUBLISH_CHOICE)
	category = models.ForeignKey(Category)

class Comment(models.Model):
	user = models.ForeignKey(User)
	blog = models.ForeignKey(BlogTable)
	description = models.TextField(max_length=500)
	created_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

class Rating(models.Model):
	rating = models.FloatField(max_length=50)
	blog = models.ForeignKey(BlogTable)
	user = models.ForeignKey(User)
	created_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

