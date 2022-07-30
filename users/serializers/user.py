from rest_framework import serializers

from SITAbackend.custom_serializer import DynamicFieldSerializerMixin


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(max_length=256, required=False)
    last_name = serializers.CharField(max_length=256, required=False)

    class Meta:
        fields = "__all__"


class EmailLoginSerializer(DynamicFieldSerializerMixin, serializers.Serializer):
    """
    Serializer for user email login
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        fields = (
            "email",
            "password",
        )


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    EMAIL_LOGIN = "EMAIL_LOGIN"
    LOGIN_TYPES = [EMAIL_LOGIN]

    action = serializers.ChoiceField(required=True, choices=LOGIN_TYPES)
    payload = serializers.DictField(required=True)

    def to_internal_value(self, value):
        login_type = value.get("action")

        if login_type == self.EMAIL_LOGIN:
            self.fields["payload"] = EmailLoginSerializer(data=value.get("payload"))

        return super().to_internal_value(value)
