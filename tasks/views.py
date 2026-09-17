from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from accounts.permissions import IsAdmin
from .filters import TaskFilter
from .models import Task
from .permissions import IsAdminOrReadOnly
from .serializers import (
    TaskCreateUpdateSerializer,
    TaskReorderSerializer,
    TaskSerializer,
    TaskStatusUpdateSerializer,
)
from . import services


class TaskListCreateView(ListCreateAPIView):
  

    queryset = Task.objects.all().select_related("created_by")
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = TaskFilter
    ordering_fields = ["due_date", "order", "created_at", "priority"]
    ordering = ["order"]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TaskCreateUpdateSerializer
        return TaskSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def perform_create(self, serailizer):
        # Auto-set the ordr to the end of the list
        last_ordr = Task.objects.count()
        serailizer.save(created_by=self.request.user, order=last_ordr)


class TaskDetailView(RetrieveUpdateDestroyAPIView):
  

    queryset = Task.objects.all().select_related("created_by")
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            if self.request.user.is_staff:
                return TaskCreateUpdateSerializer
            return TaskStatusUpdateSerializer
        return TaskSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def update(self, request, *args, **kwargs):
        # Normal users can only PATCH, and only the status field
        if not request.user.is_staff and request.method == "PUT":
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)


class TaskReorderView(APIView):
  

    permission_classes = [IsAdmin]

    def post(self, request):
        serailizer = TaskReorderSerializer(data=request.data)
        serailizer.is_valid(raise_exception=True)

        orderd_ids = serailizer.validated_data["ordered_ids"]
        services.reorder_tasks(orderd_ids)

        return Response({"detail": "Tasks reordered successfully."}, status=status.HTTP_200_OK)


class TaskExportExcelView(APIView):
 

    permission_classes = [IsAuthenticated]

    def get(self, request):
        quryset = Task.objects.all().order_by("order")
        return services.get_excel_response(quryset)


class TaskExportPDFView(APIView):
  

    permission_classes = [IsAuthenticated]

    def get(self, request):
        quryset = Task.objects.all().order_by("order")
        return services.get_pdf_response(quryset)
