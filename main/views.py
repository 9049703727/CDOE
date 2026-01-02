from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.http import Http404
from django.template import TemplateDoesNotExist
from django.core.mail import send_mail
from django.conf import settings
from .models import Notification

from .models import Course, Category, Instructor, Inquiry
from .forms import ContactForm


# =========================
# Home Page
# =========================
def index(request):
    return render(request, 'index.html')


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
        'category', 'instructor', 'instructor__user'
    )

    categories = request.GET.getlist('category')
    levels = request.GET.getlist('level')
    durations = request.GET.getlist('duration')
    price_filter = request.GET.getlist('price')
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'popular')

    if categories and 'all' not in categories:
        courses = courses.filter(category__slug__in=categories)

    if levels and 'all' not in levels:
        courses = courses.filter(level__in=levels)

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
            Q(instructor__user__first_name__icontains=search_query) |
            Q(instructor__user__last_name__icontains=search_query)
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
def course_enroll(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)

    if request.method == 'POST':
        messages.success(request, f'Successfully enrolled in {course.title}!')
        return redirect('course_detail', slug=course.slug)

    return render(request, 'enroll.html', {'course': course})


# =========================
# Inquiry Form (UPDATED)
# =========================
def inquiry_form(request):
    if request.method == "POST":

        inquiry = Inquiry.objects.create(
            course=request.POST.get('course'),
            first_name=request.POST.get('firstName'),
            middle_name=request.POST.get('middleName'),
            last_name=request.POST.get('lastName'),
            gender=request.POST.get('gender'),
            category=request.POST.get('category'),
            dob=request.POST.get('dob'),
            email=request.POST.get('email'),
            mobile=request.POST.get('mobile'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            pin=request.POST.get('pin'),
            country=request.POST.get('country'),
            qualification=request.POST.get('qualification'),
            passing_year=request.POST.get('passingYear'),
            stream=request.POST.get('stream'),
            current_status=request.POST.get('currentStatus'),
        )

        # =========================
        # Email to USER
        # =========================
        send_mail(
            subject="Inquiry Received – Gujarat University Online Education",
            message=f"""
Dear {inquiry.first_name} {inquiry.last_name},

Thank you for your inquiry for the "{inquiry.course}" course.

We have received your request successfully.
Our team will contact you shortly with further details.

Regards,
Gujarat University Online Education Team
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[inquiry.email],
            fail_silently=False,
        )

        # =========================
        # Email to ADMIN
        # =========================
        send_mail(
            subject="New Inquiry Submitted",
            message=f"""
New Inquiry Details:

Name: {inquiry.first_name} {inquiry.last_name}
Email: {inquiry.email}
Mobile: {inquiry.mobile}
Course: {inquiry.course}
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )

        return redirect('inquiry_success')

    return render(request, 'inquiry.html')


# =========================
# Inquiry Success Page
# =========================
def inquiry_success(request):
    return render(request, 'inquiry_success.html')

def iks_course_registration(request):
    return render(request,'iks_course_registration')


def index(request):
    notifications = Notification.objects.all().order_by('-date')[:5]
    return render(request, 'index.html', {
        'notifications': notifications
    })

# View all notifications page
def notifications_view(request):
    notifications = Notification.objects.all().order_by('-date')
    return render(request, 'notifications.html', {
        'notifications': notifications
    })


def technical_staff(request):
    staff_list = TechnicalStaff.objects.filter(is_active=True)
    return render(request, 'technical_staff.html', {
        'staff_list': staff_list
    })