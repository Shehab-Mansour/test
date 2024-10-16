from rest_framework import serializers, viewsets
from .models import users
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = users  # تأكد من أن `users` هو النموذج الصحيح
        fields = ['username', 'email', 'password', 'birthday', 'state']
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = users(
            username=validated_data['username'],
            email=validated_data['email'],
            birthday=validated_data['birthday'],
            state=validated_data['state']
        )
        user.password = make_password(validated_data['password'])
        user.save()
        return user



class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = '__all__'