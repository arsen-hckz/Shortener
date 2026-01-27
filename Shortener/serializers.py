from .models import ShortLink , ClickEvent
from rest_framework import serializers






class ShortLinkSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()
    custom_code = serializers.CharField(required = False)
    class Meta:
        model = ShortLink
        fields = ['long_url','custom_code','code','short_url','created_at']
        read_only_fields = ['created_at','short_url','code']

    def get_short_url(self,obj):
        base = self.context["base_url"].rstrip("/")
        return f"{base}/{obj.code}"

