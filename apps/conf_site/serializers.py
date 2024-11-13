from rest_framework import serializers
from apps.conf_site.models import Service, SubmitRequest, ServiceBlog
from apps.conf_site.utils import check_email_or_phone


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'image', 'created_at']


class SubmitRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmitRequest
        fields = ['id', 'full_name', 'phone', 'email', 'topic', 'deadline', 'created_at']

    def validate(self, data):
        contact_value = data.get('phone') or data.get('email')

        if contact_value:
            result = check_email_or_phone(contact_value)
            if result == 'invalid':
                raise serializers.ValidationError("Invalid phone or email format.")

            if result == 'email' and data.get('phone'):
                data['phone'] = None
            if result == 'phone' and data.get('email'):
                data['email'] = None

        return data


class ServiceBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceBlog
        fields = ['id', 'name', 'text', 'url', 'created_at']