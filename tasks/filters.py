from django_filters import rest_framework as filters

from .models import Task


class TaskFilter(filters.FilterSet):
    # Search by name or code via ?search=
    search = filters.CharFilter(method="filter_by_name_or_code", label="Search")

    # Filter by exact status or priority
    status = filters.ChoiceFilter(choices=Task.STATUS_CHOICES)
    priority = filters.ChoiceFilter(choices=Task.PRIORITY_CHOICES)

    # Date range filters for due_date
    due_date_from = filters.DateFilter(field_name="due_date", lookup_expr="gte")
    due_date_to = filters.DateFilter(field_name="due_date", lookup_expr="lte")

    class Meta:
        model = Task
        fields = ["status", "priority", "due_date_from", "due_date_to"]

    def filter_by_name_or_code(self, queryset, name, value):
        return queryset.filter(name__icontains=value) | queryset.filter(
            code__icontains=value
        )
