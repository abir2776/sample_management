from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from organizations.models import UserCompany
from organizations.rest.serializers.users import CompanyUserSerializer


class CompanyUserListCreateView(ListCreateAPIView):
    serializer_class = CompanyUserSerializer

    def get_queryset(self):
        organization = self.request.user.get_company()
        queryset = UserCompany.objects.filter(organization=organization)
        return queryset


class CompanyUserDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = CompanyUserSerializer
    queryset = UserCompany.objects.filter()
    lookup_field = "uid"
