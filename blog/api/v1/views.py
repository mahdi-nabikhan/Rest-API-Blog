from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from blog.api.v1.serializers import *
from blog.models import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics
from rest_framework import viewsets


class CategoryListCreate(APIView):
    """
    getting a list of post and creating a new category
    """
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        categories = Category.objects.all()
        serializer = self.serializer_class(categories, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListCreation(APIView):
    """
    getting a list of post and creating the new post
    """
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        post = Posts.objects.all()
        serializer = PostSerializer(post, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    """
    getting the single post and updated the post and delete the post
    """
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, pk):
        post = Posts.objects.get(pk=pk)
        serializer = self.serializer_class(post, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        data = request.data
        obj = Posts.objects.get(pk=pk)

        serializer = self.serializer_class(obj, data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        data = request.data
        obj = Posts.objects.get(pk=pk)
        serializer = self.serializer_class(obj, data=data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = Posts.objects.get(pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostListGeneric(generics.ListCreateAPIView):
    """
    getting list of post and creating a new post (with generic method)
    """
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Posts.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostDetailGeneric(generics.RetrieveUpdateDestroyAPIView):
    """
    getting the single post and updating the post and delete the post (using generic method)
    """
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Posts.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CategoryListCreateGeneric(generics.ListCreateAPIView):
    """
    getting list of post and creating a new category (with generic method)
    """
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostCRUDViewSet(viewsets.ViewSet):
    """
    CRUD operation for post (using ViewSet)
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Posts.objects.all()

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        obj = Posts.objects.get(pk=pk)
        serializer = self.serializer_class(obj, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        obj = Posts.objects.get(pk=pk)
        data = request.data
        serializer = self.serializer_class(obj, data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        obj = Posts.objects.get(pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        obj = Posts.objects.get(pk=pk)
        data = request.data
        serializer = self.serializer_class(instance=obj, data=data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryCRViewSet(viewsets.ViewSet):
    """ list and create and retrieve methods for category (using ViewSet) """
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Category.objects.all()

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        obj = Category.objects.get(pk=pk)
        serializer = self.serializer_class(obj, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
