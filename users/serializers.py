from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class EmailSerializer(serializers.Serializer):
    # email = serializers.CharField(max_length=None, min_length=None)
    email = serializers.EmailField()
    # confirmation_code = serializers.CharField(max_length=None, min_length=None, allow_null=True)


class TokenGainSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(max_length=100)

# class UserSerializer(serializers.Serializer):
class UserSerializer(serializers.ModelSerializer):

    # def create(self, validated_data):
    #     user = User.objects.create(validated_data)
    #     user.save()
    #     return user
    def create(self, validated_data):
        return User.objects.create(**validated_data)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "bio", "email", "role"]
