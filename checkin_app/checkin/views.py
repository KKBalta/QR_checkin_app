from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from .models import Workplace, AttendanceLog, User, APIKey 
from .forms import WorkplaceForm, UserRegistrationForm
from geopy.distance import geodesic  # To calculate distance
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import Group
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from functools import wraps

def group_required(*group_names):
    def in_groups(user):
        if user.is_authenticated:
            if bool(user.groups.filter(name__in=group_names)) | user.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)

@login_required
@group_required('Admin', 'manager')
def add_workplace(request):
    if request.method == 'POST':
        form = WorkplaceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('workplace_list')
    else:
        form = WorkplaceForm()
    return render(request, 'checkin/add_workplace.html', {'form': form})

@login_required
@group_required('Admin', 'manager', 'Employee')
def workplace_list(request):
    workplaces = Workplace.objects.all()
    recent_logs = AttendanceLog.objects.filter(employee=request.user).order_by('-check_in_time')[:5]
    return render(request, 'checkin/workplace_list.html', {
        'workplaces': workplaces,
        'recent_logs': recent_logs,
        'is_checked_in': request.user.is_checked_in
    })

@login_required
@group_required('Employee')
@transaction.atomic
def checkin_checkout(request, workplace_id):
    workplace = get_object_or_404(Workplace, id=workplace_id)

    # Check if latitude and longitude are provided in the request
    user_latitude = request.POST.get('latitude')
    user_longitude = request.POST.get('longitude')

    if user_latitude and user_longitude:
        user_latitude = Decimal(user_latitude).quantize(Decimal('1.00000000'), rounding=ROUND_HALF_UP)
        user_longitude = Decimal(user_longitude).quantize(Decimal('1.00000000'), rounding=ROUND_HALF_UP)
        user_location = (float(user_latitude), float(user_longitude))
        
        # Ensure workplace has valid latitude and longitude
        if workplace.latitude is None or workplace.longitude is None:
            return render(request, 'checkin/error.html', {
                "message": "Workplace location is not set.",
                "workplace_name": workplace.name,
                "current_time": now()
            })
        
        workplace_location = (float(workplace.latitude), float(workplace.longitude))

        # Calculate distance
        distance = geodesic(user_location, workplace_location).meters  # Distance in meters
        
        if distance > 100:  # Allow check-in within a 100m radius
            return render(request, 'checkin/error.html', {
                "message": "You are not at the correct location.",
                "workplace_name": workplace.name,
                "current_time": now()
            })

        if not request.user.is_checked_in:
            # If the user is not checked in, create a new attendance log for check-in
            log = AttendanceLog.objects.create(
                employee=request.user,
                workplace=workplace,
                check_in_time=now(),
                checkin_latitude=user_latitude,
                checkin_longitude=user_longitude
            )
            request.user.is_checked_in = True
            request.user.save()
            return render(request, 'checkin/success.html', {
                "message": "Checked in successfully.",
                "workplace_name": workplace.name,
                "current_time": now()
            })
        else:
            # If the user is already checked in, update the existing attendance log for check-out
            log = AttendanceLog.objects.filter(employee=request.user, workplace=workplace, check_out_time=None).first()
            if log:
                log.check_out_time = now()
                log.save()
                request.user.is_checked_in = False
                request.user.save()
                return render(request, 'checkin/success.html', {
                    "message": "Checked out successfully.",
                    "workplace_name": workplace.name,
                    "current_time": now()
                })
            else:
                return render(request, 'checkin/error.html', {
                    "message": "No active check-in found.",
                    "workplace_name": workplace.name,
                    "current_time": now()
                })
    else:
        # If latitude and longitude are not provided, render a page to get the user's location
        return render(request, 'checkin/get_location.html', {'workplace_id': workplace_id})

@login_required
@group_required('Admin', 'Manager')
def weekly_report(request, user_id):
    user = get_object_or_404(User, id=user_id)
    end_date = now().date()
    start_date = end_date - timedelta(days=7)
    logs = AttendanceLog.objects.filter(employee=user, check_in_time__date__range=[start_date, end_date])

    total_hours = sum(log.hours_worked() for log in logs if log.hours_worked() is not None)

    context = {
        'user': user,
        'logs': logs,
        'total_hours': total_hours,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'checkin/weekly_report.html', context)

@login_required
@group_required('Admin', 'Manager')
def generate_report(request):
    end_date = now().date()
    start_date = end_date - timedelta(days=7)
    logs = AttendanceLog.objects.filter(check_in_time__date__range=[start_date, end_date])

    context = {
        'logs': logs,
        'start_date': start_date,
        'end_date': end_date,
    }

    html_string = render_to_string('checkin/report.html', context)
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="report.pdf"'
    return response

def api_key_required(view_func):
    """Decorator to check if a valid API key is provided."""
    @wraps(view_func)
    def _wrapped_view_func(request, *args, **kwargs):
        api_key = request.headers.get("X-API-KEY")  # Get API key from request header
        
        # Check if the API key exists and is active in the database
        if not api_key or not APIKey.objects.filter(key=api_key, is_active=True).exists():
            return JsonResponse({"error": "Unauthorized"}, status=401)
        
        return view_func(request, *args, **kwargs)  # Continue with the view
    return _wrapped_view_func

@csrf_exempt
@api_key_required
def api_report(request):
    try:
        # Get days from header, default to 1 if not provided
        days = int(request.headers.get('X-DAYS', 1))
        if days < 1:
            return JsonResponse({"error": "Days must be greater than 0"}, status=400)
            
        end_date = now().date()
        start_date = end_date - timedelta(days=days)
        logs = AttendanceLog.objects.filter(check_in_time__date__range=[start_date, end_date])

        data = {
            'logs': [
                {
                    'employee': log.employee.username,
                    'workplace': log.workplace.name,
                    'check_in_time': log.check_in_time,
                    'check_out_time': log.check_out_time,
                    'hours_worked': log.hours_worked(),
                }
                for log in logs
            ],
            'start_date': start_date,
            'end_date': end_date,
            'days_requested': days
        }

        return JsonResponse(data)
        
    except ValueError:
        return JsonResponse({"error": "Invalid days value"}, status=400)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            employee_group = Group.objects.get(name='Employee')
            user.groups.add(employee_group)
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('login')  # Redirect to home page after successful registration
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'auth/register.html', {'form': form})

def redirect_to_login(request):
    return redirect(reverse('login'))