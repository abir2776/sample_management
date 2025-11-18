from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from organizations.models import OrganizationUser
from organizations.rest.serializers.users import OrganizationUserSerializer


class OrganizationUserListCreateView(ListCreateAPIView):
    serializer_class = OrganizationUserSerializer

    def get_queryset(self):
        organization = self.request.user.get_organization()
        queryset = OrganizationUser.objects.filter(organization=organization)
        return queryset


class OrganizationUserDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrganizationUserSerializer
    queryset = OrganizationUser.objects.filter()
    lookup_field = "uid"
