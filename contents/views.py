from rest_framework.views import APIView, Response, status
from django.forms import model_to_dict
from contents.models import Content
from contents.content_serializer import ContentSerializer

class ContentView(APIView):
    def get(self, request):

        contents = Content.objects.all()

        contents_list = [model_to_dict(content) for content in contents]

        return Response(contents_list)

    def post(self, request):

        serializer = ContentSerializer(**request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        content = Content.objects.create(**serializer.validate_data)
        serializer = ContentSerializer(content)

        return Response(serializer.data, status.HTTP_201_CREATED)

class ContentDetailView(APIView):

    def get(self, request, content_id: int):

        try:
            content = Content.objects.get(id=content_id)
        except content.DoesNotExist:
            return Response({"details": "content not found"}, status.HTTP_404_NOT_FOUND)

        content_dict = model_to_dict(content)

        return Response(content_dict)

    def patch(self, request, content_id: int):
        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({"details": "Content not found"}, status.HTTP_404_NOT_FOUND)

        for key, value in request.data.items():
            setattr(content, key, value)

        content.save()

        content_dict = model_to_dict(content)

        return Response(content_dict, status.HTTP_200_OK)

    def delete(self, request, content_id: int):
        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({"details": "Content not found"}, status.HTTP_404_NOT_FOUND)

        content.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ContentSearchView(APIView):
    def get(self, request):

        title_param = request.query_params.get("title")

        contents = Content.objects.filter(
            title__contains=title_param
        )

        filtered_contents = [model_to_dict(content) for content in contents]

        return Response(filtered_contents, status.HTTP_200_OK)