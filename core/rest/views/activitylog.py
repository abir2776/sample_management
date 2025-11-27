from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from core.rest.serializers.activitylog import ActivityLogSerializer
from organizations.models import ActivityLog
from sample_manager.permissions import IsSuperAdmin


class ActivityLogListCreateView(ListCreateAPIView):
    serializer_class = ActivityLogSerializer
    queryset = ActivityLog.objects.filter()

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsSuperAdmin()]

        return [IsAuthenticated()]
