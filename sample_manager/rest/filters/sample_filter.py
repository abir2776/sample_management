from django_filters import rest_framework as filters

from sample_manager.models import GarmentSample


class GarmentSampleFilter(filters.FilterSet):
    weight_min = filters.NumberFilter(field_name="weight", lookup_expr="gte")
    weight_max = filters.NumberFilter(field_name="weight", lookup_expr="lte")
    size_cen_min = filters.NumberFilter(field_name="size_cen", lookup_expr="gte")
    size_cen_max = filters.NumberFilter(field_name="size_cen", lookup_expr="lte")
    color = filters.CharFilter(field_name="color", lookup_expr="iexact")
    size = filters.CharFilter(field_name="size", lookup_expr="iexact")
    types = filters.CharFilter(field_name="types", lookup_expr="iexact")
    buyer = filters.CharFilter(method="filter_by_buyer")
    project = filters.CharFilter(method="filter_by_project")

    class Meta:
        model = GarmentSample
        fields = [
            "color",
            "size",
            "types",
            "weight_min",
            "weight_max",
            "size_cen_min",
            "size_cen_max",
            "buyer",
            "category",
            "sub_category",
            "project",
        ]

    def filter_by_buyer(self, queryset, name, value):
        from sample_manager.models import SampleBuyerConnection

        sample_ids = SampleBuyerConnection.objects.filter(buyer__uid=value).values_list(
            "sample_id", flat=True
        )
        return queryset.filter(id__in=sample_ids)

    def filter_by_project(self, queryset, name, value):
        from sample_manager.models import ProjectSample

        sample_ids = ProjectSample.objects.filter(project__uid=value).values_list(
            "sample_id", flat=True
        )
        return queryset.filter(id__in=sample_ids)
