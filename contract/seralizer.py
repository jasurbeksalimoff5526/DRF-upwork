from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from project.models import IN_PROGRESS, OPEN, Project

from .models import ACCEPTED, ACTIVE, FINISHED, PENDING, REJECTED, Bid, Contract, Review


class BidSerializer(serializers.ModelSerializer):
    freelancer = serializers.StringRelatedField(read_only=True)
    project_title = serializers.ReadOnlyField(source="project.title")

    class Meta:
        model = Bid
        fields = ["id", "project", "project_title", "freelancer", "price", "message", "status", "created_at"]
        read_only_fields = ["id", "project", "project_title", "freelancer", "status", "created_at"]

    def validate(self, attrs):
        project = self.context["project"]
        user = self.context["request"].user

        if project.status != OPEN:
            raise ValidationError({"project": "Faqat open statusdagi projectga bid yuborish mumkin."})
        if project.client == user:
            raise ValidationError({"project": "Client o'z projectiga bid yubora olmaydi."})
        if Bid.objects.filter(project=project, freelancer=user).exists():
            raise ValidationError({"project": "Bu projectga allaqachon bid yuborgansiz."})
        return attrs

    def create(self, validated_data):
        return Bid.objects.create(
            project=self.context["project"],
            freelancer=self.context["request"].user,
            **validated_data,
        )


class BidListSerializer(serializers.ModelSerializer):
    freelancer = serializers.StringRelatedField(read_only=True)
    freelancer_id = serializers.UUIDField(source="freelancer.id", read_only=True)

    class Meta:
        model = Bid
        fields = ["id", "freelancer", "freelancer_id", "price", "message", "status", "created_at"]


class ContractSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField(read_only=True)
    freelancer = serializers.StringRelatedField(read_only=True)
    project_title = serializers.ReadOnlyField(source="project.title")

    class Meta:
        model = Contract
        fields = [
            "id",
            "project",
            "project_title",
            "client",
            "freelancer",
            "agreed_price",
            "status",
            "created_at",
            "finished_at",
        ]
        read_only_fields = fields


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "contract", "rating", "comment", "created_at"]
        read_only_fields = ["id", "contract", "created_at"]

    def validate(self, attrs):
        contract = self.context["contract"]
        if contract.status != FINISHED:
            raise ValidationError({"contract": "Review faqat finished contract uchun yoziladi."})
        if hasattr(contract, "review"):
            raise ValidationError({"contract": "Bu contract uchun review allaqachon yozilgan."})
        return attrs

    def create(self, validated_data):
        return Review.objects.create(contract=self.context["contract"], **validated_data)


def accept_bid(bid):
    with transaction.atomic():
        bid = Bid.objects.select_for_update().select_related("project", "freelancer", "project__client").get(pk=bid.pk)
        project = bid.project

        if project.status != OPEN:
            raise ValidationError({"project": "Bu project uchun freelancer allaqachon tanlangan."})
        if bid.status != PENDING:
            raise ValidationError({"bid": "Faqat pending bid qabul qilinadi."})

        Bid.objects.filter(project=project).exclude(pk=bid.pk).update(status=REJECTED)
        bid.status = ACCEPTED
        bid.save(update_fields=["status", "updated_at"])

        project.status = IN_PROGRESS
        project.save(update_fields=["status", "updated_at"])

        contract = Contract.objects.create(
            project=project,
            client=project.client,
            freelancer=bid.freelancer,
            agreed_price=bid.price,
            status=ACTIVE,
        )
        return contract
