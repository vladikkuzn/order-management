from rest_framework import serializers

from users_app.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class for User model.
    """

    def create(self, validated_data):
        """
        Method to create new user instance
        """

        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'role')
        extra_kwargs = {
            'password': {'write_only': True},
        }
