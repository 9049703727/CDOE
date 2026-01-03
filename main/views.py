from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum, Avg
from django.contrib import messages
from django.http import Http404
from django.template import TemplateDoesNotExist
from django.core.mail import send_mail
from django.conf import settings
from .models import Notification

from .models import Course, Category, Instructor
from .forms import ContactForm
from .models import TechnicalStaff




# =========================
# Home Page
# =========================


def index(request):
    # Get featured courses (you can customize the criteria)

     # Get featured courses (active courses, ordered by newest)
    featured_courses = Course.objects.filter(is_active=True).order_by('-created_at')[:3]
    notifications = Notification.objects.all().order_by('-date')[:5]
        
    # Get all categories with course count
    # categories = Category.objects.annotate(
    #     course_count=Count('courses', filter=models.Q(courses__is_active=True))
    # ).filter(course_count__gt=0)[:8]
    
    # Get featured instructors
    featured_instructors = Instructor.objects.filter(
        is_active=True,
    )[:4]

    context = {
        'notifications' : notifications,
        'featured_courses': featured_courses,
        # 'categories': categories,
        'featured_instructors': featured_instructors,
              
    }
    return render(request, 'index.html',context)


# =========================
# Contact Page
# =========================
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd['email'],
                [getattr(settings, 'DEFAULT_FROM_EMAIL', 'webmaster@localhost')],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent. Thank you!')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


# =========================
# Static HTML Pages
# =========================
def serve_html(request, filename):
    template_name = f"{filename}.html"
    try:
        return render(request, template_name)
    except TemplateDoesNotExist:
        raise Http404()


# =========================
# Course List Page
# =========================
def courses_list(request):
    courses = Course.objects.filter(is_active=True).select_related(
        'category', 'instructor'
    )

    categories = request.GET.getlist('category')
    levels = request.GET.getlist('level')
    durations = request.GET.getlist('duration')
    price_filter = request.GET.getlist('price')
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'popular')

    if 'all' in categories:
        categories = []
    
    # Filter courses
    courses = Course.objects.all()
    
    if categories:
        courses = courses.filter(category__slug__in=categories)

    # if levels and 'all' not in levels:
    #     courses = courses.filter(level__in=levels)

    if durations:
        duration_q = Q()
        if 'under_5' in durations:
            duration_q |= Q(duration_hours__lt=5)
        if '5_20' in durations:
            duration_q |= Q(duration_hours__gte=5, duration_hours__lte=20)
        if 'over_20' in durations:
            duration_q |= Q(duration_hours__gt=20)
        courses = courses.filter(duration_q)

    if price_filter:
        if 'free' in price_filter and 'paid' not in price_filter:
            courses = courses.filter(is_free=True)
        elif 'paid' in price_filter and 'free' not in price_filter:
            courses = courses.filter(is_free=False)

    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(instructor__first_name__icontains=search_query) |
            Q(instructor__last_name__icontains=search_query)
        )

    if sort_by == 'popular':
        courses = courses.order_by('-students_enrolled')
    elif sort_by == 'newest':
        courses = courses.order_by('-created_at')
    elif sort_by == 'price_low':
        courses = courses.order_by('price')
    elif sort_by == 'price_high':
        courses = courses.order_by('-price')
    elif sort_by == 'duration_short':
        courses = courses.order_by('duration_hours')

    paginator = Paginator(courses, 6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'all_categories': Category.objects.all(),
        'selected_categories': categories,
        'selected_levels': levels,
        'selected_durations': durations,
        'selected_price': price_filter,
        'search_query': search_query,
        'sort_by': sort_by,
        'total_courses': paginator.count,
    }

    return render(request, 'courses.html', context)


# =========================
# Course Detail Page
# =========================
def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)

    related_courses = Course.objects.filter(
        category=course.category,
        is_active=True
    ).exclude(id=course.id)[:3]

    return render(request, 'course-details.html', {
        'course': course,
        'related_courses': related_courses,
    })


# =========================
# Course Enrollment Page
# =========================
# def course_enroll(request, slug):
#     course = get_object_or_404(Course, slug=slug, is_active=True)

#     if request.method == 'POST':
#         messages.success(request, f'Successfully enrolled in {course.title}!')
#         return redirect('course_detail', slug=course.slug)

#     return render(request, 'enroll.html', {'course': course})

def course_enroll(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)
    courses = Course.objects.filter(is_active=True).order_by("title")

    return render(
        request,
        "enroll.html",
        {
            "course": course,     # for auto-selection
            "courses": courses,   # for dropdown
        }
    )


def instructors_list(request):
    """View for listing all instructors"""
    # Get all active instructors
    instructors = Instructor.objects.filter(is_active=True)
    
    # Get filter parameters
    specialization = request.GET.get('specialization', '')
    search_query = request.GET.get('search', '')
    
    # Apply specialization filter
    if specialization:
        instructors = instructors.filter(specialization__icontains=specialization)
    
    # Apply search
    if search_query:
        instructors = instructors.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(specialization__icontains=search_query) |
            Q(bio__icontains=search_query)
        )
    
    # Annotate with course count and total students
    instructors = instructors.annotate(
        course_count=Count('courses', filter=Q(courses__is_active=True)),
        total_students_count=Sum('courses__students_enrolled', filter=Q(courses__is_active=True)),
        avg_rating=Avg('courses__rating', filter=Q(courses__is_active=True))
    )
    
    # Order by featured first, then by name
    instructors = instructors.order_by('-is_featured', 'first_name')
    
    # Pagination
    paginator = Paginator(instructors, 8)  # 8 instructors per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Get unique specializations for filter
    all_specializations = Instructor.objects.filter(
        is_active=True
    ).exclude(
        specialization=''
    ).values_list('specialization', flat=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'all_specializations': all_specializations,
        'selected_specialization': specialization,
        'search_query': search_query,
        'total_instructors': paginator.count,
    }
    
    return render(request, 'instructors.html', context)


def instructor_detail(request, id):
    """View for individual instructor profile"""
    instructor = get_object_or_404(Instructor, id=id, is_active=True)
    
    # Get instructor's courses
    courses = Course.objects.filter(
        instructor=instructor,
        is_active=True
    ).select_related('category')
    
    # Calculate stats
    total_courses = courses.count()
    total_students = courses.aggregate(Sum('students_enrolled'))['students_enrolled__sum'] or 0
    avg_rating = courses.aggregate(Avg('rating'))['rating__avg'] or 0
    
    context = {
        'instructor': instructor,
        'courses': courses,
        'total_courses': total_courses,
        'total_students': total_students,
        'avg_rating': round(avg_rating, 1),
    }
    
    return render(request, 'instructor-profile.html', context)
# =========================
# Inquiry Form (FINAL FIXED)
# =========================
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json, random, time

from .models import  Course

OTP_EXPIRY_SECONDS = 300  # 5 minutes

# =========================
# SUCCESS PAGE
# =========================
def inquiry_success(request):
    return render(request, "inquiry_success.html")


def iks_course_registration(request):
    return render(request, 'iks_course_registration.html')



# View all notifications page
def notifications_view(request):
    notifications = Notification.objects.all().order_by('-date')
    return render(request, 'notifications.html', {
        'notifications': notifications
    })
def technical_staff(request):
    staff_list = TechnicalStaff.objects.filter(is_active=True)
    print("STAFF COUNT:", staff_list.count())

    return render(request, 'technical_staff.html', {
        'staff_list': staff_list
    })


