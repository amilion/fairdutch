from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from spliter.api.serializers import SplitSerializer
from spliter.models import Split


class SplitView(APIView):
    serializer_class = SplitSerializer

    def get_queryset(self):
        return Split.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(
            instance=queryset, many=True, allow_empty=True
        )
        return Response(data={"splits": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class()
        serializer.create()
        return Response(
            data={"message": "dutches splited successfully!"},
            status=status.HTTP_201_CREATED,
        )
