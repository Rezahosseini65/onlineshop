from rest_framework import serializers

from onlineshop.auths.users.models import OTPrequest


class OTPRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=12,allow_null=False)
    channel = serializers.ChoiceField(allow_null=False,choices=OTPrequest.OTPChannel.choices)

class ResponceOTPRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPrequest
        fields = ['request_id']

class VerifyOTPRequestSerializer(serializers.Serializer):
    request_id = serializers.CharField(max_length=40,allow_null=False)
    phone = serializers.CharField(max_length=12, allow_null=False)
    password = serializers.CharField(style={'input_type':'password'},max_length=4,allow_null=False)

class VerifyOTPResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_user = serializers.BooleanField()
