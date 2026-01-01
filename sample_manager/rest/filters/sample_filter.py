from django_filters import rest_framework as filters

from sample_manager.models import GarmentSample

LETTER_SIZE_MAP = {
    "XXS": 1,
    "XS": 2,
    "S": 3,
    "M": 4,
    "L": 5,
    "XL": 6,
    "XXL": 7,
    "2XL": 7,
    "3XL": 8,
    "4XL": 9,
    "5XL": 10,
}


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
    letter_range_min = filters.CharFilter(method="filter_letter_min")
    letter_range_max = filters.CharFilter(method="filter_letter_max")

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
            "letter_range_min",
            "letter_range_max",
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

    def filter_letter_min(self, queryset, name, value):
        value = value.upper()
        mapped_value = LETTER_SIZE_MAP.get(value)

        if mapped_value is None:
            return queryset.none()

        return queryset.filter(letter_range_min__lte=mapped_value)

    def filter_letter_max(self, queryset, name, value):
        value = value.upper()
        mapped_value = LETTER_SIZE_MAP.get(value)

        if mapped_value is None:
            return queryset.none()

        return queryset.filter(letter_range_max__gte=mapped_value)
