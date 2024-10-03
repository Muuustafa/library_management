from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Book, User, Loan
from .serializers import BookSerializer, UserSerializer, LoanSerializer
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
      # Fonction pour récupérer les 6 derniers livres disponibles
    @action(detail=False, methods=['get'], url_path='latest-available')
    def latest_available(self, request):
        # Filtrer les livres disponibles, trier par ID décroissant et limiter à 6
        available_books = Book.objects.filter(availability=True).order_by('-id')[:6]
        serializer = self.get_serializer(available_books, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    user_data = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'profile_image': user.profile_image.url if user.profile_image else None,
    }
    return Response(user_data)


@api_view(['GET'])
def get_available_books(request):
    books = Book.objects.filter(availability=True).order_by('-id')[:6]
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)