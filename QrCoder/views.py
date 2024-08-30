from django.contrib.auth.models import Group, User
from django.http import HttpResponse, HttpResponseNotFound
from QrCoder.models import QrCode
from rest_framework import permissions, viewsets

from QrCoder.serializers import GroupSerializer, UserSerializer, QrCodeSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class QrCodeViewSet(viewsets.ModelViewSet):
    queryset = QrCode.objects.all().order_by('encodedInfo')
    serializer_class = QrCodeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return QrCode.objects.filter(user=self.request.user)
        return QrCode.objects.all()

def serve_qr_code_image(request, image_name):
    try:
        #test if provided image_name is linked to request user
        if(not QrCode.objects.filter(user=request.user).exists()):
            return HttpResponseNotFound('Image not found')

        qr_code = QrCode.objects.get(image__contains=image_name)
        qr_code.image.open()
        image = qr_code.image.read()
        response = HttpResponse(image, content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="%s"' % image_name

        return response
    except QrCode.DoesNotExist:
        return HttpResponseNotFound('Image not found')