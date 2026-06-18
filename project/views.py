from django.db.models import Q
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination

from shared.permissions import IsClientOrReadOnly

from .models import OPEN, Project
from .serializer import ProjectSerializer


class ProjectPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class ProjectListCreateAPIView(ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsClientOrReadOnly]
    pagination_class = ProjectPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]

    def get_queryset(self):
        queryset = Project.objects.all()

        if self.request.method == "GET":
            queryset = queryset.filter(status=OPEN)

        min_budget = self.request.query_params.get("min_budget")
        max_budget = self.request.query_params.get("max_budget")
        budget = self.request.query_params.get("budget")

        if budget:
            queryset = queryset.filter(budget=budget)
        if min_budget:
            queryset = queryset.filter(budget__gte=min_budget)
        if max_budget:
            queryset = queryset.filter(budget__lte=max_budget)

        search = self.request.query_params.get("q")
        if search:
            queryset = queryset.filter(Q(title__icontains=search))

        return queryset.order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class ProjectDetailAPIView(RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
