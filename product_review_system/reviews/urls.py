from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'reviews'

# Create a router for product and review views
router = DefaultRouter()

urlpatterns = [
    # Product endpoints
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:product_id>/reviews/', views.ReviewListView.as_view(), name='review-list'),
    path('products/<int:product_id>/reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    path('products/<int:product_id>/stats/', views.ProductReviewsStatsView.as_view(), name='product-stats'),
]
