from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum, Avg
from django.contrib import messages
from django.http import Http404
from django.template import TemplateDoesNotExist
from django.core.mail import send_mail
from django.conf import settings
from .models import Notification

from .models import Course, Category, Instructor, Testimonial
from .forms import ContactForm
from .models import TechnicalStaff
from .models import AdminStaff
from .models import FAQ
from .models import IKSRegistration






# =========================
# Home Page
# =========================


def index(request):
    # Get featured courses (you can customize the criteria)

     # Get featured courses (active courses, ordered by newest)
    featured_courses = Course.objects.filter(is_active=True).order_by('-created_at')[:3]
    notifications = Notification.objects.all().order_by('-date')[:5]
    testimonials = Testimonial.objects.filter(is_active=True)
        
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
        'testimonials': testimonials
              
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
from .models import Inquiry, Course

import json
import random
import time

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import Inquiry, Course

OTP_EXPIRY_SECONDS = 300  # 5 minutes


# ==================================================
# INQUIRY FORM (OTP PROTECTED, MULTI-COURSE)
# ==================================================
import json
import random
import time
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def inquiry_form(request):
    courses = Course.objects.filter(is_active=True).order_by("title")
    
    if request.method == "POST":
        # Get the email from form
        email = request.POST.get("email")
        print("Processing inquiry for email:", email)

        # Check if OTP was verified for this specific email
        if not request.session.get("otp_verified", False):
            return render(
                request,
                "enroll.html",
                {
                    "courses": courses,
                    "error": "Please verify your email with OTP first.",
                    "email": email
                }
            )

        # Verify the email matches the one that was verified
        verified_email = request.session.get("email_for_otp", "")
        if email != verified_email:
            return render(
                request,
                "enroll.html",
                {
                    "courses": courses,
                    "error": "Email doesn't match verified email. Please verify again.",
                    "email": email
                }
            )

        # Multiple courses selection
        course_slugs = request.POST.getlist("courses")

        if not course_slugs:
            return render(
                request,
                "enroll.html",
                {
                    "courses": courses,
                    "error": "Please select at least one course."
                }
            )

        course_objs = Course.objects.filter(
            slug__in=course_slugs,  # Fixed: use __in for multiple values
            is_active=True
        )

        if not course_objs.exists():
            return render(
                request,
                "enroll.html",
                {
                    "courses": courses,
                    "error": "Invalid course selection."
                }
            )

        # Create Inquiry
        inquiry = Inquiry.objects.create(
            first_name=request.POST.get("firstName"),
            middle_name=request.POST.get("middleName"),
            last_name=request.POST.get("lastName"),
            gender=request.POST.get("gender"),
            date_of_birth=request.POST.get("dateOfBirth"),
            email=request.POST.get("email"),
            mobile_number=request.POST.get("mobileNumber"),
            nationality=request.POST.get("nationality"),
            country=request.POST.get("country"),
            state=request.POST.get("state"),
            pincode=request.POST.get("pincode"),
        )

        # Save ManyToMany courses
        inquiry.courses.add(*course_objs)

        # Course names for email
        course_titles = ", ".join(course.title for course in course_objs)

        # Email to USER
        try:
            send_mail(
                subject="Inquiry Received – Gujarat University Online Education",
                message=f"""Dear {inquiry.first_name} {inquiry.last_name},

Thank you for your inquiry.

Selected Courses:
{course_titles}

We have received your request successfully.
Our team will contact you shortly.

Regards,
CDOE Online Education Team""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[inquiry.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending user email: {e}")

        # Email to ADMIN
        try:
            send_mail(
                subject="New Inquiry Submitted",
                message=f"""New Inquiry Details:

Name: {inquiry.first_name} {inquiry.last_name}
Email: {inquiry.email}
Mobile: {inquiry.mobile_number}
Courses: {course_titles}""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending admin email: {e}")

        # Clear OTP session
        for key in ["email_otp", "otp_time", "otp_verified", "email_for_otp"]:
            request.session.pop(key, None)

        return redirect("inquiry_success")
    
    return render(request, "enroll.html", {"courses": courses})


# Send OTP
@require_POST
def send_otp(request):
    try:
        data = json.loads(request.body)
        email = data.get("email")
        
        if not email:
            return JsonResponse({"status": "error", "message": "Email is required"})
        
        print("Sending OTP to email:", email)
        
        # Generate 6-digit OTP
        email_otp = str(random.randint(100000, 999999))
        
        # Store in session
        request.session["email_otp"] = email_otp
        request.session["otp_time"] = time.time()
        request.session["otp_verified"] = False
        request.session["email_for_otp"] = email
        request.session.modified = True  # Force session save
        
        print(f"OTP stored in session: {email_otp}")
        
        # Send email
        try:
            send_mail(
                subject="Email Verification OTP",
                message=f"Your OTP is {email_otp}. Valid for 5 minutes.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            print("Email sent successfully")
        except Exception as e:
            print(f"Email sending failed: {e}")
            return JsonResponse({"status": "error", "message": f"Failed to send email: {str(e)}"})
        
        return JsonResponse({"status": "success", "message": "OTP sent successfully"})
    
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"})
    except Exception as e:
        print(f"Error sending OTP: {e}")
        return JsonResponse({"status": "error", "message": str(e)})


# Verify OTP
@require_POST
def verify_otp(request):
    try:
        data = json.loads(request.body)
        user_otp = data.get("emailOtp", "").strip()
        
        print(f"Verifying OTP: {user_otp}")
        
        # Check if OTP was sent
        if "email_otp" not in request.session:
            return JsonResponse({"status": "error", "message": "OTP not requested. Please request OTP first."})
        
        # Check OTP expiry
        otp_time = request.session.get("otp_time", 0)
        current_time = time.time()
        time_diff = current_time - otp_time
        
        print(f"OTP age: {time_diff} seconds")
        
        if time_diff > 300:  # 5 minutes
            # Clear expired OTP
            for key in ["email_otp", "otp_time", "otp_verified", "email_for_otp"]:
                request.session.pop(key, None)
            return JsonResponse({"status": "expired", "message": "OTP expired. Please request a new one."})
        
        # Verify OTP
        stored_otp = request.session.get("email_otp", "")
        print(f"Stored OTP: {stored_otp}, User OTP: {user_otp}")
        
        if user_otp == stored_otp:
            request.session["otp_verified"] = True
            request.session.modified = True
            print("OTP verified successfully")
            return JsonResponse({"status": "verified", "message": "OTP verified successfully"})
        else:
            return JsonResponse({"status": "invalid", "message": "Invalid OTP. Please try again."})
    
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"})
    except Exception as e:
        print(f"Error verifying OTP: {e}")
        return JsonResponse({"status": "error", "message": str(e)})


# Inquiry Success Page
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



def admin_staff_list(request):
    staff_list = AdminStaff.objects.filter(is_active=True)
    

    return render(request, 'administration.html', {
        'staff_list': staff_list
    })



def contact_page(request):
    faqs = FAQ.objects.filter(is_active=True)
    
    context = {
        'faqs': faqs,
        # Include your contact form here as well
        # 'form': YourContactForm(),  # replace with your form
    }
    return render(request, 'contact.html', context)



