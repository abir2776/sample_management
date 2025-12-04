from rest_framework.generics import (
    RetrieveAPIView,
)

from core.rest.serializers.users import UserSerializer


class UserProfileView(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
