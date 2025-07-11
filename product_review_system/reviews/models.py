from django.db import models
from django.db.models import Avg, F
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Product(models.Model):
    """Product model to store product information."""
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products_created',
        verbose_name=_('created by')
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('product')
        verbose_name_plural = _('products')
    
    def __str__(self):
        return self.name
    
    @property
    def average_rating(self):
        """Calculate and return the average rating of the product."""
        return self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
    
    @property
    def review_count(self):
        """Return the total number of reviews for the product."""
        return self.reviews.count()

class Review(models.Model):
    """Review model to store user reviews for products."""
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('product')
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('user')
    )
    rating = models.PositiveSmallIntegerField(
        _('rating'),
        choices=RATING_CHOICES,
        help_text=_('Rating from 1 (Poor) to 5 (Excellent)')
    )
    comment = models.TextField(_('comment'), blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('review')
        verbose_name_plural = _('reviews')
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'user'],
                name='unique_product_user_review',
                violation_error_message=_('You have already reviewed this product.')
            ),
            models.CheckConstraint(
                check=models.Q(rating__gte=1) & models.Q(rating__lte=5),
                name='rating_range',
                violation_error_message=_('Rating must be between 1 and 5.')
            )
        ]
    
    def __str__(self):
        return f"{self.user.email}'s review for {self.product.name}"
    
    def save(self, *args, **kwargs):
        """Override save to ensure only regular users can create reviews."""
        if not hasattr(self, 'user') or not self.user.role == User.Role.REGULAR:
            raise ValueError(_('Only regular users can create reviews.'))
        super().save(*args, **kwargs)
