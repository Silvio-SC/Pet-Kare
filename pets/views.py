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
        trait = req.query_params.get("trait", None)
        if trait:
            try:
                pets = Pet.objects.filter(traits__name__iexact=trait)
                print(pets[0])
            except IndexError:
                pets = []
            result_page = self.paginate_queryset(pets, req, view=self)
            serializer = PetSerializer(result_page, many=True)
        else:
            pets = Pet.objects.all()
            result_page = self.paginate_queryset(pets, req, view=self)
            serializer = PetSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class PetDateilView(APIView):
    def get(self, req: Request, pet_id: int) -> Response:
        try:
            pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, 404)

        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, req: Request, pet_id: int) -> Response:
        try:
            pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, 404)

        pet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, req: Request, pet_id: int) -> Response:
        try:
            pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, 404)

        serializer = PetSerializer(data=req.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        trait_data = req.data.get('traits')
        group_data = req.data.get('group')

        if trait_data:
            trait_list = []
            for trait in req.data["traits"]:
                name = trait["trait_name"]
                print(trait)

                try:
                    find_traits = Trait.objects.filter(name__iexact=name)[0]
                except IndexError:
                    find_traits = Trait.objects.create(**{"name": name})
                
                trait_list.append(find_traits)
        
            pet.traits.set(trait_list)

        if group_data:
            name = group_data["scientific_name"]

            try:
                find_group = Group.objects.filter(scientific_name__iexact=name)[0]
            except IndexError:
                find_group = Group.objects.create(**req.data["group"])

            pet.group = find_group

        for key, value in serializer.validated_data.items():
            if key == "group" or key == "traits":
                continue
            setattr(pet, key, value)

        pet.save()

        serializer = PetSerializer(pet)

        return Response(serializer.data, 200)
