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
    #
    # first_name = serializers.CharField(max_length=200, required=False)
    # last_name = serializers.CharField(max_length=200, required=False)
    # username = serializers.CharField(max_length=200, )
    # bio = serializers.CharField(max_length=200, required=False)
    # email = serializers.EmailField()
    # role = serializers.CharField(max_length=200,required=False, default='user')

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "bio", "email", "role"]
