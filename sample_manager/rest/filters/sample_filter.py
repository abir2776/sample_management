from django_filters import rest_framework as filters

from sample_manager.models import GarmentSample


class GarmentSampleFilter(filters.FilterSet):
    weight_min = filters.NumberFilter(field_name="weight", lookup_expr="gte")
    weight_max = filters.NumberFilter(field_name="weight", lookup_expr="lte")
    age_range_year_max = filters.NumberFilter(
        field_name="age_range_year_max", lookup_expr="gte"
    )
    age_range_year_min = filters.NumberFilter(
        field_name="age_range_year_min", lookup_expr="lte"
    )
    age_range_month_max = filters.NumberFilter(
        field_name="age_range_month_max", lookup_expr="gte"
    )
    age_range_month_min = filters.NumberFilter(
        field_name="age_range_month_min", lookup_expr="lte"
    )
    color = filters.CharFilter(field_name="color", lookup_expr="iexact")
    category = filters.CharFilter(field_name="category", lookup_expr="iexact")
    sub_category = filters.CharFilter(field_name="sub_category", lookup_expr="iexact")
    types = filters.CharFilter(field_name="types", lookup_expr="iexact")
    buyer = filters.CharFilter(method="filter_by_buyer")
    project = filters.CharFilter(method="filter_by_project")
    letter_range_max = filters.NumberFilter(
        field_name="letter_range_max", lookup_expr="gte"
    )
    letter_range_min = filters.NumberFilter(
        field_name="letter_range_min", lookup_expr="lte"
    )

    class Meta:
        model = GarmentSample
        fields = [
            "color",
            "types",
            "weight_min",
            "weight_max",
            "age_range_year_max",
            "age_range_year_min",
            "age_range_month_max",
            "age_range_month_min",
            "buyer",
            "category",
            "sub_category",
            "project",
            "letter_range_max",
            "letter_range_min",
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
