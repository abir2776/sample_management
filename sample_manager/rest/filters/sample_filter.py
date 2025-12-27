from django_filters import rest_framework as filters

from sample_manager.models import GarmentSample


class GarmentSampleFilter(filters.FilterSet):
    weight_min = filters.NumberFilter(field_name="weight", lookup_expr="gte")
    weight_max = filters.NumberFilter(field_name="weight", lookup_expr="lte")
    size_cen_min = filters.NumberFilter(field_name="size_cen", lookup_expr="gte")
    size_cen_max = filters.NumberFilter(field_name="size_cen", lookup_expr="lte")
    color = filters.CharFilter(field_name="color", lookup_expr="iexact")
    size = filters.CharFilter(field_name="size", lookup_expr="iexact")
    category = filters.CharFilter(field_name="category", lookup_expr="iexact")
    sub_category = filters.CharFilter(field_name="sub_category", lookup_expr="iexact")
    types = filters.CharFilter(field_name="types", lookup_expr="iexact")
    buyer = filters.CharFilter(method="filter_by_buyer")
    project = filters.CharFilter(method="filter_by_project")
    age_range_min = filters.NumberFilter(method="filter_by_age_range_min")
    age_range_max = filters.NumberFilter(method="filter_by_age_range_max")

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
            "age_range_min",
            "age_range_max",
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

    def filter_by_age_range_min(self, queryset, name, value):
        """
        Filter samples where the size_range maximum is >= the given minimum age.
        Example: if age_range_min=5, includes "4-10 Y" (max=10 >= 5)
        """
        import re

        filtered_ids = []
        for sample in queryset:
            if sample.size_range:
                # Extract numbers from size_range (e.g., "4-10 Y" -> [4, 10])
                numbers = re.findall(r"\d+", sample.size_range)
                if numbers:
                    # Get the maximum value from the range
                    max_age = max(int(num) for num in numbers)
                    if max_age >= value:
                        filtered_ids.append(sample.id)

        return queryset.filter(id__in=filtered_ids)

    def filter_by_age_range_max(self, queryset, name, value):
        """
        Filter samples where the size_range minimum is <= the given maximum age.
        Example: if age_range_max=8, includes "4-10 Y" (min=4 <= 8)
        """
        import re

        filtered_ids = []
        for sample in queryset:
            if sample.size_range:
                # Extract numbers from size_range (e.g., "4-10 Y" -> [4, 10])
                numbers = re.findall(r"\d+", sample.size_range)
                if numbers:
                    # Get the minimum value from the range
                    min_age = min(int(num) for num in numbers)
                    if min_age <= value:
                        filtered_ids.append(sample.id)

        return queryset.filter(id__in=filtered_ids)
