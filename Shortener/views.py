from django.shortcuts import render

import hashlib
from django.shortcuts import get_object_or_404 ,redirect
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDate
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .models import ShortLink,ClickEvent
from  .serializers import ShortLinkSerializer
from .utils import base62_encode
from django.conf import settings
from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework import status





#checking if the custom code already exists in db
class CodeExists(APIView):
    authentication_classes=[]
    permission_classes = []
    def get(self,request,code:str):
        exists = ShortLink.objects.filter(code = code ).exists()
        return Response({"code":code,"Available":not exists})
    

class CreateShortLinkView(APIView):
    def post(self,request):
        serializer = ShortLinkSerializer(data = request.data,context = {"base_url" : settings.BASE_URL})

        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        long_url = data["long_url"]
        custome_code = data.get("custom_code")

        if custome_code:
            try:
                with transaction.atomic():
                    link = ShortLink.objects.create(
                        code = custome_code,
                        long_url = long_url
                    )
            except IntegrityError:
                return Response({"message":"Custome code is already in use "},status=status.HTTP_409_CONFLICT)
        else: 
            link = ShortLink.objects.create(
                code = "tmp",
                long_url = long_url
            )
            link.code = base62_encode(link.id)
            link.save(update_fields=["code"])
        return Response(ShortLinkSerializer(link ,context = {"base_url",settings.BASE_URL}).data,status=status.HTTP_201_CREATED)
    



class RedirectAndTrack(APIView):
    permission_classes = []
    authentication_classes = []
    
    def get(self,request,code):
        link = get_object_or_404(ShortLink,code = code ,is_active = True)
        if link.expires_at and link.expires_at < timezone.now():
         return Response({"message": "Link expired"}, status=410)
        ip = request.META.get("REMOTE_ADDR","")
        salt = timezone.now().strftime("%Y-%m-%d")
        ip_hash = hashlib.sha256(f"{salt}:{ip}".encode().hexidest() if ip else "")

        ClickEvent.objects.create(
            link = link,
            ip_hash = ip_hash
            user_agent = request.META.get("HTTP_USER_AGENT","")
            referer = request.META.get("HTTP_REFERER","")
        )

        return redirect(link.long_url)
    


class LinkStats(APIView):
    
    permission_classes = []
    authentication_classes = []

    def get(self,request,code):
        
        link = get_object_or_404(ShortLink, code = code , is_active= True)
        daily = (
            link.clicks
            .annotate(day=TruncDate("ts"))
            .values("day")
            .annotate(clicks=Count("id"))
            .order_by("day")
        )
        return Response(
            {
                "code":code,
                "long_url":link.long_url,
                "total_clicks":link.clicks.count(),
                "daily":list(daily)
            },status=200
        )


