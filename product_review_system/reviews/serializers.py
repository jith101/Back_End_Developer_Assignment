from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from .models import Product, Review
from users.serializers import UserSerializer

class ProductListSerializer(serializers.ModelSerializer):
    """Serializer for listing products with basic information."""
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        help_text='Price of the product (must be greater than 0)'
    )
    average_rating = serializers.FloatField(
        read_only=True,
        help_text='Average rating of the product (1-5)'
    )
    review_count = serializers.IntegerField(
        read_only=True,
        help_text='Number of reviews for this product'
    )
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'average_rating', 'review_count')
        read_only_fields = ('id', 'average_rating', 'review_count')

class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer for product details."""
    created_by = UserSerializer(read_only=True)
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        help_text='Price of the product (must be greater than 0)'
    )
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'created_at', 
                 'updated_at', 'created_by', 'average_rating', 'review_count')
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by', 
                          'average_rating', 'review_count')

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for reviews."""
    user = UserSerializer(read_only=True)
    can_edit = serializers.SerializerMethodField()
    rating = serializers.IntegerField(
        min_value=1,
        max_value=5,
        help_text='Rating value from 1 to 5',
        validators=[
            MinValueValidator(1, message='Rating must be at least 1'),
            MaxValueValidator(5, message='Rating cannot be more than 5')
        ]
    )
    
    class Meta:
        model = Review
        fields = ('id', 'product', 'user', 'rating', 'comment', 
                 'created_at', 'updated_at', 'can_edit')
        read_only_fields = ('id', 'product', 'user', 'created_at', 'updated_at')
    
    def get_can_edit(self, obj):
        """
        Determine if the current user can edit this review.
        Only the review creator can edit their own review.
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.user == request.user
        return False

class ProductWithReviewsSerializer(ProductDetailSerializer):
    """Serializer for product details with reviews."""
    reviews = serializers.SerializerMethodField()
    
    class Meta(ProductDetailSerializer.Meta):
        fields = ProductDetailSerializer.Meta.fields + ('reviews',)
    
    def get_reviews(self, obj):
        """Get paginated reviews for the product."""
        from rest_framework.pagination import PageNumberPagination
        from rest_framework.request import Request
        
        reviews = obj.reviews.all().order_by('-created_at')
        
        # Get the request from the context
        request = self.context.get('request')
        if not request or not isinstance(request, Request):
            return []
        
        # Paginate the reviews
        paginator = PageNumberPagination()
        paginator.page_size = 5  # Show 5 reviews per page
        page = paginator.paginate_queryset(reviews, request)
        
        # Serialize the paginated reviews
        serializer = ReviewSerializer(
            page, 
            many=True,
            context={'request': request}
        )
        
        # Add pagination info to the response
        response = paginator.get_paginated_response(serializer.data)
        return response.data

class CreateProductSerializer(serializers.ModelSerializer):
    """Serializer for creating a new product."""
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        help_text='Price of the product (must be greater than 0)'
    )
    
    class Meta:
        model = Product
        fields = ('name', 'description', 'price')
    
    def create(self, validated_data):
        """Set the created_by field to the current user."""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
