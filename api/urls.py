from django.urls import path, include  # type: ignore
from rest_framework.routers import DefaultRouter  # type: ignore
from .views import AuthorViewSet, BookViewSet, CustomerViewSet, OrderViewSet
from .auth_views import AuthorRegistrationView, AuthorLoginView, CustomerRegistrationView, CustomerLoginView  # Import your new views

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('authors/register/', AuthorRegistrationView.as_view(), name='author-register'),  # Registration for authors
    path('authors/login/', AuthorLoginView.as_view(), name='author-login'),  # Login for authors
    path('customers/register/', CustomerRegistrationView.as_view(), name='customer-register'),  # Registration for customers
    path('customers/login/', CustomerLoginView.as_view(), name='customer-login'),  # Login for customers
]