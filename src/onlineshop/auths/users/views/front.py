from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.authtoken.models import Token
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from onlineshop.auths.users.models import OTPrequest
from onlineshop.auths.users.serializers.front import OTPRequestSerializer, ResponceOTPRequestSerializer, VerifyOTPResponseSerializer,\
    VerifyOTPRequestSerializer

class TwicePerMinuteThrottle(UserRateThrottle):
    rate = '2/minute'
class RequestOTPView(APIView):
    throttle_classes = [TwicePerMinuteThrottle]
    def post(self,request):
        serializer = OTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            otp_req = OTPrequest()
            otp_req.phone = serializer.validated_data['phone']
            otp_req.channel = serializer.validated_data['channel']
            otp_req.generate_password()
            otp_req.save()
            return Response(ResponceOTPRequestSerializer(otp_req).data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPRequestView(APIView):
    def post(self,request):
        serializer = VerifyOTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            otp_request = OTPrequest.objects.filter(request_id = serializer.validated_data['request_id'],
                                            phone = serializer.validated_data['phone'],
                                            valid_until__gte=timezone.now())

            if not otp_request:
                return Response(status=status.HTTP_404_NOT_FOUND)
            User = get_user_model()
            flag = True
            try :
                user = User.objects.get(username = serializer.validated_data['phone'])
                flag = False
            except :
                user = User.objects.create(username = serializer.validated_data['phone'])
            token, created = Token.objects.get_or_create(user=user)
            return Response(data=VerifyOTPResponseSerializer({'token': token, 'new_user': flag}).data)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
