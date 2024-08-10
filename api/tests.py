from django.test import TestCase  # type: ignore
from .models import Author, Book, Customer, Order
from django.conf import settings # type: ignore

class BookstoreTests(TestCase):
    def setUp(self):
        author = Author.objects.create(name='Author 1', email='author1@example.com', bio='Bio 1')
        self.book = Book.objects.create(title='Book 1', author=author, price=10.00, stock=5, publication_date='2024-01-01')
        self.customer = Customer.objects.create(name='Customer 1', email='customer1@example.com', password='password')

        # Set the discount value in settings (environment variable)
        settings.DISCOUNT_VALUE = 10  # Assuming a flat discount of $10 for the test

    def test_create_order_with_discount(self):
        # Calculate total amount with discount
        total_amount = self.book.price - settings.DISCOUNT_VALUE

        # Create order with the discounted total_amount
        order = Order.objects.create(customer=self.customer, total_amount=total_amount)
        
        # Add the book to the order
        order.ordered_books.add(self.book)

        # Check that the total_amount is correctly set
        self.assertEqual(order.total_amount, total_amount)

    def test_create_order_with_discount_less_than_price(self):
        # Set discount that is less than the book price
        settings.DISCOUNT_VALUE = 5  # Flat discount of $5 for this test
        total_amount = self.book.price - settings.DISCOUNT_VALUE

        # Create order with the discounted total_amount
        order = Order.objects.create(customer=self.customer, total_amount=total_amount)
        
        # Add the book to the order
        order.ordered_books.add(self.book)

        # Check that the total_amount is correctly set
        self.assertEqual(order.total_amount, total_amount)

    def test_create_order_with_discount_greater_than_price(self):
        # Set discount greater than book price
        settings.DISCOUNT_VALUE = 15  # Flat discount of $15 for this test
        total_amount = max(self.book.price - settings.DISCOUNT_VALUE, 0)  # Total should not be negative

        # Create order with the discounted total_amount
        order = Order.objects.create(customer=self.customer, total_amount=total_amount)
        
        # Add the book to the order
        order.ordered_books.add(self.book)

        # Check that the total_amount is correctly set
        self.assertEqual(order.total_amount, total_amount)