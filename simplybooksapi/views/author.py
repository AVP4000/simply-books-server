from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from simplybooksapi.models import Author

class AuthorSerializer(serializers.ModelSerializer):
    """JSON serializer for Author"""
    class Meta:
        model = Author
        fields = ('id', 'email', 'first_name', 'last_name', 'image', 'favorite', 'uid')

class AuthorView(ViewSet):
    """Level up author s view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single author 

        Returns:
            Response -- JSON serialized author 
        """
        author = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all authors 

        Returns:
            Response -- JSON serialized list of author 
        """
        author = Author.objects.all()
        
        uid = request.query_params.get('uid', None)
        
        if uid is not None:
            author = author.filter(uid=uid)
            
            
        serializer = AuthorSerializer(author, many=True)
        return Response(serializer.data)
   
    # Creates the book 
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        author = Author.objects.create(
            email=request.data["email"],
            uid=request.data["uid"],
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
            image=request.data["image"],
            favorite=request.data["favorite"],
        )
        serializer = AuthorSerializer(author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a book"""

        # Fetch the book to be updated
        author = Author.objects.get(pk=pk)

    

        # Update book details
        author.email = request.data["email"]
        author.first_name = request.data["first_name"]
        author.last_name = request.data["last_name"]
        author.image = request.data["image"]
        author.uid = request.data["uid"]
        author.favorite = request.data["favorite"]
        author.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    # Delete book 
    def destroy(self, request, pk):
        author = Author.objects.get(pk=pk)
        author.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)