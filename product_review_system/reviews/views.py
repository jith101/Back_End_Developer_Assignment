from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from .models import Product, Review
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    ProductWithReviewsSerializer,
    ReviewSerializer,
    CreateProductSerializer
)
from users.models import User

class ProductListView(generics.ListCreateAPIView):
    """
    API endpoint that allows listing all products or creating a new product.
    """
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateProductSerializer
        return ProductListSerializer
    
    def get_queryset(self):
        # Allow filtering by search query parameter
        queryset = Product.objects.all()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows viewing, updating, or deleting a product.
    """
    queryset = Product.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductWithReviewsSerializer
        return ProductDetailSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
    
    def get_object(self):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        if self.request.method == 'GET':
            # For GET requests, we want to include reviews in the response
            return product
        return product

class ReviewListView(generics.ListCreateAPIView):
    """
    API endpoint that allows listing all reviews for a product or creating a new review.
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(product_id=product_id).order_by('-created_at')
    
    def perform_create(self, serializer):
        product = get_object_or_404(Product, pk=self.kwargs['product_id'])
        # Check if user has already reviewed this product
        if Review.objects.filter(product=product, user=self.request.user).exists():
            raise ValidationError({"detail": _("You have already reviewed this product.")})
        
        serializer.save(user=self.request.user, product=product)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows viewing, updating, or deleting a review.
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_id'])
    
    def get_object(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs['pk'],
            product_id=self.kwargs['product_id']
        )
        return review
    
    def perform_update(self, serializer):
        # Only allow the review author to update their own review
        if serializer.instance.user != self.request.user:
            raise PermissionDenied({"detail": _("You do not have permission to edit this review.")})
        serializer.save()
    
    def perform_destroy(self, instance):
        # Only allow the review author to delete their own review
        if instance.user != self.request.user:
            raise PermissionDenied({"detail": _("You do not have permission to delete this review.")})
        instance.delete()

class ProductReviewsStatsView(APIView):
    """
    API endpoint that provides statistics about product reviews.
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        
        # Get review statistics
        reviews = product.reviews.all()
        total_reviews = reviews.count()
        average_rating = reviews.aggregate(avg_rating=models.Avg('rating'))['avg_rating'] or 0
        
        # Get rating distribution
        rating_distribution = {i: 0 for i in range(1, 6)}
        for review in reviews:
            rating_distribution[review.rating] += 1
        
        return Response({
            'product_id': product_id,
            'product_name': product.name,
            'total_reviews': total_reviews,
            'average_rating': round(average_rating, 1),
            'rating_distribution': rating_distribution
        })
