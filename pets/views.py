from rest_framework.views import Request, Response, APIView, status
from .serializers import PetSerializer
from traits.models import Trait
from groups.models import Group
from .models import Pet
from rest_framework.pagination import PageNumberPagination


class PetView(APIView, PageNumberPagination):
    def post(self, req: Request) -> Response:
        serializer = PetSerializer(data=req.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        group_data = serializer.validated_data.pop('group')
        traits_data = serializer.validated_data.pop('traits')

        try:
            find_group = Group.objects.filter(
                scientific_name__contains=group_data["scientific_name"]
            )[0]
        except IndexError:
            find_group = None

        if not find_group:
            find_group = Group.objects.create(**group_data)

        pet = Pet.objects.create(**serializer.validated_data, group=find_group)

        list_trait = []
        for trait in traits_data:
            name = trait["name"]
            try:
                find_traits = Trait.objects.filter(name__iexact=name)[0]
            except IndexError:
                find_traits = Trait.objects.create(**trait)

            list_trait.append(find_traits)

        pet.traits.set(list_trait)

        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, req: Request) -> Response:
        pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, req, view=self)
        serializer = PetSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class PetDateilView(APIView):
    pass
