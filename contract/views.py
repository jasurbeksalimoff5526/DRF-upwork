from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from project.models import Project
from shared.permissions import IsContractClient, IsContractParticipant, IsFreelancer, IsProjectClient

from .models import Bid, Contract
from .seralizer import BidListSerializer, BidSerializer, ContractSerializer, ReviewSerializer, accept_bid


class BidCreateAPIView(CreateAPIView):
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated, IsFreelancer]

    def get_project(self):
        return get_object_or_404(Project, pk=self.kwargs["project_id"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["project"] = self.get_project()
        return context


class ProjectBidListAPIView(ListAPIView):
    serializer_class = BidListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"], client=self.request.user)
        return project.bids.all()


class AcceptBidAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, bid_id, *args, **kwargs):
        bid = get_object_or_404(Bid.objects.select_related("project"), pk=bid_id)
        self.check_object_permissions(request, bid.project)

        contract = accept_bid(bid)
        return Response(ContractSerializer(contract).data, status=status.HTTP_201_CREATED)

    def check_object_permissions(self, request, obj):
        permission = IsProjectClient()
        if not permission.has_object_permission(request, self, obj):
            self.permission_denied(request)


class ContractListAPIView(ListAPIView):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Contract.objects.filter(Q(client=user) | Q(freelancer=user)).order_by("-created_at")


class ContractDetailAPIView(RetrieveAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, IsContractParticipant]


class FinishContractAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        contract = get_object_or_404(Contract, pk=pk)
        permission = IsContractClient()
        if not permission.has_object_permission(request, self, contract):
            self.permission_denied(request)

        contract.finish()
        return Response(ContractSerializer(contract).data, status=status.HTTP_200_OK)


class ReviewCreateAPIView(CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_contract(self):
        return get_object_or_404(Contract, pk=self.kwargs["contract_id"], client=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["contract"] = self.get_contract()
        return context
