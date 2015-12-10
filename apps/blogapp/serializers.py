from rest_framework import serializers
from blogapp.models import *
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('first_name','last_name','email','password')
		write_only_fields = ('password',)
