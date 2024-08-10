from rest_framework import serializers  # type: ignore
from .models import Book, Author, Customer, Order

class AuthorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Password is write-only

    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'bio', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        author = Author(**validated_data)
        author.set_password(validated_data['password'])  # Hash the password
        author.save()
        return author

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Password is write-only

    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        customer = Customer(**validated_data)
        customer.set_password(validated_data['password'])  # Hash the password
        customer.save()
        return customer

class OrderSerializer(serializers.ModelSerializer):
    order_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)  # Read-only

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['order_date']  # Ensure order_date is read-only