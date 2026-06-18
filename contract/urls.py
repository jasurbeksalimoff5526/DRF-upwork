from django.urls import path

from .views import (
    AcceptBidAPIView,
    BidCreateAPIView,
    ContractDetailAPIView,
    ContractListAPIView,
    FinishContractAPIView,
    ProjectBidListAPIView,
    ReviewCreateAPIView,
)


urlpatterns = [
    path("projects/<uuid:project_id>/bids/", BidCreateAPIView.as_view(), name="bid-create"),
    path("projects/<uuid:project_id>/bids/list/", ProjectBidListAPIView.as_view(), name="project-bid-list"),
    path("bids/<uuid:bid_id>/accept/", AcceptBidAPIView.as_view(), name="bid-accept"),
    path("contracts/", ContractListAPIView.as_view(), name="contract-list"),
    path("contracts/<uuid:pk>/", ContractDetailAPIView.as_view(), name="contract-detail"),
    path("contracts/<uuid:pk>/finish/", FinishContractAPIView.as_view(), name="contract-finish"),
    path("contracts/<uuid:contract_id>/review/", ReviewCreateAPIView.as_view(), name="review-create"),
]
