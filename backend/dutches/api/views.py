from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from accounts.api.permissions import IsAuthenticated
from .serializers import DutchSerializer, DutchCUSerializer
from dutches.models import Dutch


class DutchViewSet(viewsets.ModelViewSet):
    lookup_field = "sku"

    def get_queryset(self):
        return Dutch.objects.all()

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Dutch, sku=kwargs["sku"])

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_class = ()
        else:
            permission_class = (permissions.IsAuthenticated(),)
        return permission_class

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            serializer_class = DutchSerializer
        else:
            serializer_class = DutchCUSerializer
        return serializer_class

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()
        serializer = serializer(instance=queryset, many=True)
        response = {"dutches": serializer.data}
        code = status.HTTP_200_OK
        return Response(data=response, status=code)

    def retrieve(self, request, *args, **kwargs):
        dutch = self.get_object(*args, **kwargs)
        serializer = self.get_serializer_class()
        serializer = serializer(instance=dutch, many=False)
        response = {"dutch": serializer.data}
        code = status.HTTP_200_OK
        return Response(data=response, status=code)

    def update(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        serializer = self.get_serializer_class()
        serializer = serializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(
                instance=instance, validated_data=serializer.validated_data
            )
            response = {"data": serializer.data}
            code = status.HTTP_200_OK
        else:
            response = {"message": "something went wrong!", "errors": serializer.errors}
            code = status.HTTP_400_BAD_REQUEST
        return Response(data=response, status=code)

    def create(self, request, *args, **kwargs):
        payload = request.data
        serializer = self.get_serializer_class()
        serializer = serializer(data=payload)
        if serializer.is_valid():
            serializer.create(request.user, serializer.validated_data)
            response = {"message": "dutch added successfully!", "data": serializer.data}
            code = status.HTTP_201_CREATED
        else:
            response = {"message": "something went wrong!", "errors": serializer.errors}
            code = status.HTTP_406_NOT_ACCEPTABLE
        return Response(data=response, status=code)

    def destroy(self, request, *args, **kwargs):
        dutch = self.get_object(*args, **kwargs)
        dutch.delete()
        return Response(
            data={
                "message": "deleted successfully!",
            },
            status=status.HTTP_204_NO_CONTENT,
        )
