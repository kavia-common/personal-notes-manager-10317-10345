from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note


# PUBLIC_INTERFACE
class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration including password write-only handling."""
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        # Create user with hashed password
        user = User(username=validated_data["username"], email=validated_data.get("email", ""))
        user.set_password(validated_data["password"])
        user.save()
        return user


# PUBLIC_INTERFACE
class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login payload."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


# PUBLIC_INTERFACE
class NoteSerializer(serializers.ModelSerializer):
    """Serializer for Note model."""
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Note
        fields = ("id", "title", "content", "created_at", "updated_at", "owner")
        read_only_fields = ("id", "created_at", "updated_at", "owner")
