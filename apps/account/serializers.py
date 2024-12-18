from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import ValidationError

from apps.account.models import (
    CustomUser,
)


class GroupListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name']


class CustomAuthTokenSerializer(serializers.Serializer):

    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        identifier = data.get('identifier')
        password = data.get('password')

        if not identifier or not password:
            raise serializers.ValidationError("Both email/phone and password are required")

        user_model = get_user_model()

        user = None
        if '@' in identifier:
            user = user_model.objects.filter(email=identifier).first()
        else:
            user = user_model.objects.filter(phone=identifier).first()

        if user is None:
            raise AuthenticationFailed("Invalid credentials, no user found")

        if not user.check_password(password):
            raise AuthenticationFailed("Invalid credentials, wrong password")

        return {
            'user': user
        }


class SignUpSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True, required=False)

    class Meta:
        model = get_user_model()

        fields = ['phone', 'email', 'first_name', 'last_name', 'surname', 'city', 'name_of_study', 'position', 'groups',
                  'password', 'password_confirm']

    def validate(self, data):

        if data['password'] != data['password_confirm']:
            raise ValidationError({"password_confirm": "Пароли не совпадают"})

        return data

    def create(self, validated_data):

        validated_data.pop('password_confirm', None)

        groups_data = validated_data.pop('groups', [])

        user = get_user_model().objects.create_user(
            phone=validated_data['phone'],
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            surname=validated_data.get('surname'),
            city=validated_data.get('city'),
            name_of_study=validated_data.get('name_of_study'),
            position=validated_data.get('position'),
            password=validated_data['password']
        )

        if groups_data:
            user.groups.set(groups_data)

        user.save()
        return user


class CustomUserDeatilSerializer(serializers.ModelSerializer):
    groups = GroupListSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            'id', 'phone', 'email', 'first_name', 'last_name', 'surname',
            'city', 'name_of_study', 'position', 'groups', 'avatar'
        ]


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = [
            'phone', 'email', 'first_name', 'last_name', 'surname',
            'city', 'name_of_study', 'position', 'avatar'
        ]

        extra_kwargs = {
            'phone': {'required': False},
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'surname': {'required': False},
            'city': {'required': False},
            'name_of_study': {'required': False},
            'position': {'required': False},
            'avater': {'required': False}
        }

    def update(self, instance, validated_data):

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class PasswordUpdateSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance