from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from api.serializers import cabinet_serializers

# Cabinet API Views
from cabinet.models import TgUser, ProfileCard, Post


class TgUserViewSet(ModelViewSet):
    queryset = TgUser.objects.all()
    serializer_class = cabinet_serializers.TgUserSerializer


class ProfileCardViewSet(ModelViewSet):
    queryset = ProfileCard.objects.all()
    serializer_class = cabinet_serializers.ProfileCardSerializer

    # @action(methods=["get"], detail=False)
    def retrieve(self, request: Request, pk=None):
        queryset = ProfileCard.objects.get(user=request.user)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = cabinet_serializers.PostSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.user.id
        data = request.data.dict()
        data["user"] = user_id
        serializer = self.get_serializer(data=data)
        headers = self.get_success_headers(serializer)
        if serializer.is_valid():
            return Response(status=status.HTTP_201_CREATED, data=serializer.data, headers=headers)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"Error": serializer.errors})

    def list(self, request, *args, **kwargs):
        print(request.user)
        queryset = Post.objects.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        headers = self.get_success_headers(serializer)
        return Response(status=status.HTTP_200_OK, data=serializer.data, headers=headers)
