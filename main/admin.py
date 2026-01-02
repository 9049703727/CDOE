from django.contrib import admin
from .models import Subscriber
from .models import Inquiry 
from .models import Notification  # <-- Add this line
from .models import TechnicalStaff


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)

from django.contrib import admin
from .models import Category, Instructor, Course

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['get_full_name']
    search_fields = ['first_name', 'last_name']
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'instructor', 'price', 'is_free', 'students_enrolled', 'rating', 'is_active']
    list_filter = ['category', 'is_free', 'is_active']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_active', 'price']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'image')
        }),
        ('Course Details', {
            'fields': ('category', 'instructor','duration_hours')
        }),
        ('Pricing', {
            'fields': ('price', 'is_free')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Statistics', {
            'fields': ('students_enrolled', 'rating', 'total_reviews')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

   

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'course','gender','category','dob','email', 'mobile','city','state','country', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'mobile')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'is_new')
    list_filter = ('is_new', 'date')
    search_fields = ('title',)


@admin.register(TechnicalStaff)
class TechnicalStaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'department', 'experience_years', 'is_active')
    list_filter = ('department', 'is_active')
    search_fields = ('name', 'designation')