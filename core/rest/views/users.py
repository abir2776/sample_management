from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)

from core.models import User
from core.rest.serializers.users import UserSerializer
from sample_manager.permissions import IsSuperAdmin


class UserListCreateView(ListCreateAPIView):
    permission_classes = [IsSuperAdmin]
    serializer_class = UserSerializer
    queryset = User.objects.filter()


class UserDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperAdmin]
    serializer_class = UserSerializer
    queryset = User.objects.filter()
    lookup_field = "uid"


class UserProfileView(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
