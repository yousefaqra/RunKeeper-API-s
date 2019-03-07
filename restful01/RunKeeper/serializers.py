from rest_framework import serializers
from . models import Session
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import exceptions


class SessionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Session
        fields = (
            'distance_in_miles',
            'length_of_run',
            'pk',
            'owner',)


class UserSessionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Session
        fields = (
            'url',
            'distance_in_miles',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    sessions = UserSessionSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            'url',
            'pk',
            'username',
            'session')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "Account's disabled"
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Enter valid username or password"
                raise exceptions.ValidationError(msg)
        else:
            msg = "User name and password must be provided."
            raise exceptions.ValidationError(msg)

        return data
