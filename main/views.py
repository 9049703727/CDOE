from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.http import Http404
from django.template import TemplateDoesNotExist
from .models import Course, Category, Instructor
from .forms import ContactForm

# Create your views here.

def index(request):
    return render(request, 'index.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # send email - development uses console backend by default
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


def newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            Subscriber.objects.get_or_create(email=email)
            messages.success(request, 'Subscribed to newsletter. Thank you!')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, 'Please provide a valid email address.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
    raise Http404()


def serve_html(request, filename):
    """Serve static HTML files placed in the `templates/` directory.
    Example: requesting `/about.html` renders `templates/about.html`.
    """

    from django.template import TemplateDoesNotExist
    from django.http import Http404

    # filename is captured without .html, so add it back
    template_name = f"{filename}.html"

    try:
        return render(request, template_name)
    except TemplateDoesNotExist:
        raise Http404()

from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Course, Category

def courses_list(request):
    print("yes we are checkng for our course list............")
    # Get all active courses
    courses = Course.objects.filter(is_active=True).select_related('category', 'instructor', 'instructor__user')
    
    # Get filter parameters
    categories = request.GET.getlist('category')
    levels = request.GET.getlist('level')
    durations = request.GET.getlist('duration')
    price_filter = request.GET.getlist('price')
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'popular')
    
    # Apply category filter
    if categories and 'all' not in categories:
        courses = courses.filter(category__slug__in=categories)
    
    # Apply level filter
    if levels and 'all' not in levels:
        courses = courses.filter(level__in=levels)
    
    # Apply duration filter
    if durations:
        duration_q = Q()
        if 'under_5' in durations:
            duration_q |= Q(duration_hours__lt=5)
        if '5_20' in durations:
            duration_q |= Q(duration_hours__gte=5, duration_hours__lte=20)
        if 'over_20' in durations:
            duration_q |= Q(duration_hours__gt=20)
        courses = courses.filter(duration_q)
    
    # Apply price filter
    if price_filter:
        if 'free' in price_filter and 'paid' not in price_filter:
            courses = courses.filter(is_free=True)
        elif 'paid' in price_filter and 'free' not in price_filter:
            courses = courses.filter(is_free=False)
    
    # Apply search
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(instructor__user__first_name__icontains=search_query) |
            Q(instructor__user__last_name__icontains=search_query)
        )
    
    # Apply sorting
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
    
    # Pagination
    paginator = Paginator(courses, 6)  # 6 courses per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for filter
    all_categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'all_categories': all_categories,
        'selected_categories': categories,
        'selected_levels': levels,
        'selected_durations': durations,
        'selected_price': price_filter,
        'search_query': search_query,
        'sort_by': sort_by,
        'total_courses': paginator.count,
    }
        
    return render(request, 'courses.html', context)

def course_detail(request, slug):
    print("just checing for course details page take a look for it .......")
    """View for individual course details"""
    course = get_object_or_404(Course, slug=slug, is_active=True)
    
    # Get related courses (same category, different course)
    related_courses = Course.objects.filter(
        category=course.category,
        is_active=True
    ).exclude(id=course.id)[:3]
    
    context = {
        'course': course,
        'related_courses': related_courses,
    }
    
    return render(request, 'course-details.html', context)


def course_enroll(request, slug):
    """View for course enrollment"""
    course = get_object_or_404(Course, slug=slug, is_active=True)
    
    if request.method == 'POST':
        # Add your enrollment logic here
        # For example: create enrollment record, process payment, etc.
        
        messages.success(request, f'Successfully enrolled in {course.title}!')
        return redirect('course_detail', slug=course.slug)
    
    context = {
        'course': course,
    }
    
    return render(request, 'enroll.html', context)