from django.db import models
from django.contrib.auth.models import User

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
    # Basic Information - NO USER FIELD
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    # email = models.EmailField(unique=True)
    email = models.EmailField(null=True, blank=True)

    phone = models.CharField(max_length=20, blank=True)
    
    # Profile
    bio = models.TextField(blank=True, default='')
    profile_image = models.ImageField(upload_to='instructors/', blank=True, null=True)
    
    # Professional Info
    title = models.CharField(max_length=100, blank=True, default='', help_text="e.g., Professor, Dr., etc.")
    specialization = models.CharField(max_length=200, blank=True, default='', help_text="e.g., Web Development, Data Science")
    short_description = models.TextField(max_length=500, blank=True, default='')
    
    # Social media links
    linkedin_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    
    # Stats
    total_students = models.IntegerField(default=0, help_text="Total students taught")
    years_experience = models.IntegerField(default=0, help_text="Years of teaching experience")
    
    # Display settings
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        ordering = ['-is_featured', 'first_name']
    
    def __str__(self):
        full_name = self.get_full_name()
        if self.title:
            return f"{self.title} {full_name}"
        return full_name
    
    def get_full_name(self):
        """Get full name"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_display_name(self):
        """Get formatted display name with title"""
        return str(self)
    
    def get_total_courses(self):
        """Get total number of courses taught"""
        return self.courses.filter(is_active=True).count()
    
    def get_average_rating(self):
        """Calculate average rating across all courses"""
        from django.db.models import Avg
        result = self.courses.filter(is_active=True).aggregate(Avg('rating'))
        return round(result['rating__avg'] or 0, 1)
    
    def get_total_students(self):
        """Calculate total students across all courses"""
        from django.db.models import Sum
        result = self.courses.filter(is_active=True).aggregate(Sum('students_enrolled'))
        return result['students_enrolled__sum'] or 0
        
class Course(models.Model):
    # LEVEL_CHOICES = [
    #     ('beginner', 'Beginner'),
    #     ('intermediate', 'Intermediate'),
    #     ('advanced', 'Advanced'),
    # ]
    
    # BADGE_CHOICES = [
    #     ('best_seller', 'Best Seller'),
    #     ('new', 'New'),
    #     ('popular', 'Popular'),
    #     ('certificate', 'Certificate'),
    # ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='courses')
    # level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_free = models.BooleanField(default=False)
    duration_hours = models.IntegerField(help_text="Course duration in hours")
    image = models.ImageField(upload_to='courses/')
    # badge = models.CharField(max_length=20, choices=BADGE_CHOICES, blank=True, null=True)
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

class Inquiry(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    COURSE_CHOICES = [
        ('web-development', 'Full Stack Web Development'),
        ('data-science', 'Data Science & Analytics'),
        ('digital-marketing', 'Digital Marketing Mastery'),
        ('ui-ux-design', 'UI/UX Design Fundamentals'),
        ('cybersecurity', 'Cybersecurity Essentials'),
        ('mobile-development', 'Mobile App Development'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('obc', 'OBC'),
        ('sc', 'SC'),
        ('st', 'ST'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('student', 'Student'),
        ('employed', 'Employed'),
        ('unemployed', 'Unemployed'),
        ('other', 'Other'),
    ]

    # Course
    course = models.CharField(max_length=50, choices=COURSE_CHOICES)

    # Personal Details
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    dob = models.DateField()
    email = models.EmailField()
    mobile = models.CharField(max_length=15)

    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin = models.CharField(max_length=10)
    country = models.CharField(max_length=100)

    # Education Details
    qualification = models.CharField(max_length=150)
    passing_year = models.IntegerField()
    stream = models.CharField(max_length=150)
    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
   

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.course}"

class Testimonial(models.Model):
    # Basic Information
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200, help_text="e.g., MBA Student, Data Scientist")
    profile_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    
    # Review Content
    testimonial_text = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0, help_text="Rating out of 5")
    
    # Display Settings
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.designation}"


class Notification(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    pdf = models.FileField(upload_to='notifications/', blank=True, null=True)
    is_new = models.BooleanField(default=True)

    def __str__(self):
        return self.title
class TechnicalStaff(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='technical_staff/')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    students = models.PositiveIntegerField(default=0)
    courses = models.PositiveIntegerField(default=0)

    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name



