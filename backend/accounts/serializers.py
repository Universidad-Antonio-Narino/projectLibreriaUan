from django.db.models import Q # for queries
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from django.core.exceptions import ValidationError



class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    password = serializers.CharField(max_length=128)
    
    class Meta:
        model = User
        fields = (
            'nombre',
            'email',
            'cedula',
            'numeroTelefono',
            'password',
        )


class UserLoginSerializer(serializers.ModelSerializer):
    # to accept either username or email
    email = serializers.CharField()
    password = serializers.CharField()
    id = serializers.IntegerField(required=False, read_only=True)

    def validate(self, data):
        # user,email,password validator
        email = data.get("email", None)
        password = data.get("password", None)
        if not email and not password:
            raise ValidationError("Details not entered.")
        user = None
        # if the email has been passed
        if '@' in email:
            user = User.objects.filter(
                Q(email=email) &
                Q(password=password)
                ).distinct()
            if not user.exists():
                raise ValidationError("User credentials are not correct.")
            user = User.objects.get(email=email)
        else:
            user = User.objects.filter(
                Q(username=email) &
                Q(password=password)
            ).distinct()
            if not user.exists():
                raise ValidationError("User credentials are not correct.")
            user = User.objects.get(email=email)
        if user.ifLogged:
            raise ValidationError("User already logged in.")
        user.ifLogged = True
        data['id'] = user.id
        data['password'] = len(user.password) * "x"
        user.save()
        return data

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
        )

        read_only_fields = (
            'id',
        )