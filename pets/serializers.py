from rest_framework import serializers
from .models import SexChoices
from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        max_length=20,
        choices=SexChoices.choices,
        default=SexChoices.NOT_INFORMED
    )
    group = GroupSerializer(read_only=True, null=True)
    trait = TraitSerializer(read_only=True)
