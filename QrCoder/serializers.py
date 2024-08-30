from django.contrib.auth.models import Group, User
from django.core.files.base import ContentFile
from .models import QrCode
from rest_framework import serializers
import qrcode
import hashlib
from io import BytesIO

class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'password', 'groups']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            validated_data.pop('password')
        return super().update(instance, validated_data)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class QrCodeSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image = serializers.ImageField(read_only=True)
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = QrCode
        fields = ['id','encodedInfo', 'image', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        img = qrcode.make(validated_data['encodedInfo'])

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        imgData = buffer.getvalue()

        name = str(validated_data['user']) + '_' + hashlib.sha256(validated_data['encodedInfo'].encode()).hexdigest() + '.png'
        validated_data['image'] = ContentFile(imgData, name=name)
        print(validated_data['user'], validated_data['image'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        raise serializers.ValidationError("Updates are not allowed.")