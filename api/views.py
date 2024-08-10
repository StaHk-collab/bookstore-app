from rest_framework import status  # type: ignore
from django_filters import rest_framework as django_filters # type: ignore
from rest_framework import viewsets, filters as rest_filters # type: ignore
from rest_framework.response import Response  # type: ignore
from .models import Book, Author, Customer, Order
from .serializers import BookSerializer, AuthorSerializer, CustomerSerializer, OrderSerializer
from django_filters.rest_framework import DjangoFilterBackend  # type: ignore
from django.conf import settings  # type: ignore # Import to access settings
from django.db import transaction  # type: ignore # Import for transaction management
from rest_framework.decorators import action # type: ignore
from django.contrib.auth.hashers import make_password  # type: ignore # For password hashing
from rest_framework_simplejwt.tokens import RefreshToken  # type: ignore # For JWT tokens
from django.contrib.auth import get_user_model # type: ignore

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    @action(detail=False, methods=['post'], url_path='register') # type: ignore
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        User = get_user_model()

        try:
            author = Author.objects.get(email=email)  # Use the Author model here
            if author.check_password(password):  # Verify the provided password
                refresh = RefreshToken.for_user(author)  # Create tokens
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
        except Author.DoesNotExist:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

class BookFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter()  # For price range filtering
    publication_date = django_filters.DateFromToRangeFilter()  # For publication date range filtering

    class Meta:
        model = Book
        fields = ['price', 'publication_date']  # Specify the fields you want to filter on

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (django_filters.DjangoFilterBackend, rest_filters.SearchFilter)  # Correct imports
    filterset_class = BookFilter  # Use the defined filter set
    # search_fields = ['title', 'author__name']  # Enable searching by title and author
    
    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.query_params.get('title', None)
        author = self.request.query_params.get('author', None)

        if title:
            queryset = queryset.filter(title__icontains=title)

        if author:
            queryset = queryset.filter(author__name__icontains=author)

        return queryset

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=False, methods=['post'], url_path='register')  # Custom registration action
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='login')  # Custom login action
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        User = get_user_model()

        try:
            customer = Customer.objects.get(email=email)  # Use the Customer model here
            if customer.check_password(password):  # Verify the provided password
                refresh = RefreshToken.for_user(customer)  # Create tokens
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request):
        customer_id = request.data.get('customer_id')
        book_ids = request.data.get('book_ids')

        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        ordered_books = Book.objects.filter(id__in=book_ids)

        # Handle case where no books are found
        if not ordered_books.exists():
            return Response({"error": "No valid books found."}, status=status.HTTP_404_NOT_FOUND)

        # Check for first-time user discount
        is_first_time_user = not Order.objects.filter(customer=customer).exists()

        # Calculate total amount
        total_amount = float(sum(book.price for book in ordered_books))

        # Apply discount if the customer is a first-time user
        if is_first_time_user:
            if settings.DISCOUNT_TYPE == 'percentage':
                discount = (settings.DISCOUNT_VALUE / 100) * total_amount
            elif settings.DISCOUNT_TYPE == 'flat':
                discount = settings.DISCOUNT_VALUE
            else:
                discount = 0

            total_amount -= discount

        # Use a transaction to ensure atomicity
        with transaction.atomic():
            # Create order
            order = Order.objects.create(customer=customer, total_amount=total_amount)
            order.ordered_books.set(ordered_books)

            # Update stock and check availability
            for book in ordered_books:
                if book.stock > 0:
                    book.stock -= 1  # Decrease stock
                    book.save()
                else:
                    return Response({"error": f"Book '{book.title}' is out of stock."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = Order.objects.all()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)