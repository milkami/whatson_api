from rest_framework import serializers
from .models import AppUser, CompetitionTeams, StaticQuestion
from django.contrib.auth.hashers import make_password, check_password

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = AppUser
        fields = ['username', 'email', 'password', ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = AppUser(**validated_data)
        user.password = make_password(password)  # Hash the password before saving
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        # username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = AppUser.objects.get(email=email)
        except AppUser.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password")

        if not check_password(password, user.password):
            raise serializers.ValidationError("Invalid username or password")

        return {'user': user}


class TeamSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="team.name", default="")
    university = serializers.CharField(source="team.university", default="")
    country = serializers.CharField(source="team.country", default="")

    class Meta:
        model = CompetitionTeams
        fields = ["id", "name", "car_number", "university", "country"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'username', 'email', 'statics', 'dynamics', 'scrutineering', 'bpp', 'cm', 'ed']


class StaticQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticQuestion
        fields = ['id', 'field_name', 'max_score',]