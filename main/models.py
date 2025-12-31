from django.db import models

# Create your models here.

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='instructors/', blank=True)
    
    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    BADGE_CHOICES = [
        ('best_seller', 'Best Seller'),
        ('new', 'New'),
        ('popular', 'Popular'),
        ('certificate', 'Certificate'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='courses')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_free = models.BooleanField(default=False)
    duration_hours = models.IntegerField(help_text="Course duration in hours")
    image = models.ImageField(upload_to='courses/')
    badge = models.CharField(max_length=20, choices=BADGE_CHOICES, blank=True, null=True)
    students_enrolled = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_reviews = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_badge_display_text(self):
        if self.is_free:
            return 'Free'
        return dict(self.BADGE_CHOICES).get(self.badge, '')
    
    def get_badge_class(self):
        if self.is_free:
            return 'badge-free'
        badge_classes = {
            'new': 'badge-new',
            'certificate': 'badge-certificate',
        }
        return badge_classes.get(self.badge, '')

    def get_price_display(self):
        """Return price in Indian Rupees format"""
        if self.is_free:
            return "Free"
        return f"₹{self.price:,.0f}"