from socket import IP_DROP_MEMBERSHIP
from rest_framework.views import APIView, Response, status
from django.forms import model_to_dict
from contents.models import Content
import ipdb

class ContentView(APIView):
    def get(self, request):

        contents = Content.objects.all()

        contents_list = [model_to_dict(content) for content in contents]

        return Response(contents_list)

    def post(self, request):

        content = Content.objects.create(**request.data)

        content_dict = model_to_dict(content)

        return Response(content_dict, status.HTTP_201_CREATED)