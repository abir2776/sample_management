from rest_framework.generics import (
    RetrieveUpdateAPIView,
)

from core.rest.serializers.users import UserSerializer


class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
