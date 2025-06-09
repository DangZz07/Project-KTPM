from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import FamilyMember,Charge, Payment, Article, RoomUser, Notification
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import JsonResponse
import re


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                # Kiểm tra nếu tài khoản đã được phê duyệt
                if getattr(user, 'is_approved', False):  # `is_approved` là trường trạng thái trong model
                    login(request, user)
                    messages.success(request, "Đăng nhập thành công!")
                    return redirect('homepage')
                else:
                    # Hiển thị thông báo và render đến `wait.html` nếu chưa được phê duyệt
                    messages.warning(request, "Tài khoản của bạn đang chờ phê duyệt. Vui lòng đợi.")
                    return render(request, 'app/wait.html', {'username': user.username})
        else:
            # Hiển thị thông báo lỗi nếu thông tin đăng nhập không chính xác
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không chính xác.")
            return redirect('login')
    
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Bạn đã đăng xuất thành công.")  # Thông báo
    return redirect('login')

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        messages.success(self.request, "Tạo tài khoản thành công. Vui lòng đăng nhập.")  # Thông báo
        return super().form_valid(form)

def homepage_view(request):
    articles = Article.objects.order_by('date')
    return render(request, 'app/homepage.html', {'articles': articles})

def about(request):
    return render(request, 'app/about.html')

def contact(request):
    return render(request, 'app/contact.html')

@login_required
def notification(request):
    try:
        user = RoomUser.objects.get(username=request.user.username)
        notes = Notification.objects.filter(room_id=user.room_id).order_by('-date', '-id')
    except AttributeError:
        notes = []
    return render(request, 'app/notification.html', {'notes': notes})

@login_required
def list_member(request):
    user = request.user
    try:
        # Fetch all family members for the logged-in user's room
        family_members = FamilyMember.objects.filter(room_id=user.room_id)
    except AttributeError:
        # If `user.roomuser` or `room_id` is not accessible, log this or handle it as needed
        family_members = []

    # Pass family_members directly to the template
    return render(request, 'app/member.html', {'family_members': family_members})

@login_required
def changepassword(request):
    user = RoomUser.objects.get(username=request.user.username)
    context = {
        'room_id': user.room_id,
        'username': user.username,
        'registry_email': user.registry_email,
        'phone_number': user.phone_number
    }
    return render(request, 'app/changepassword.html', context)

@login_required
def password_change_done(request):
    return render(request, 'app/homepage.html')

@login_required
def view_payment(request):
    user = RoomUser.objects.get(username=request.user.username)
    payments = Payment.objects.filter(room_id=user.room_id)
    payment_info_list = [
        {
            'khoan_thu': payment.charge_id.name,
            'phi': payment.amount,
            'da_dong': payment.status,
            'han_nop': payment.date
        }
        for payment in payments
    ]
    return render(request, 'app/service.html', {'payment_info_list': payment_info_list})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError

@login_required
def add_member(request):
    if request.method == 'POST':
        room_user = get_object_or_404(RoomUser, username=request.user.username)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        dob = request.POST.get('date_of_birth')
        cccd = request.POST.get('cccd')  # Trường Căn cước công dân
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        # Kiểm tra dữ liệu hợp lệ
        if not (first_name and last_name and dob and email and phone_number and cccd):
            messages.error(request, "Vui lòng nhập đầy đủ thông tin hợp lệ.")
            return redirect('service')
        if not re.match(r'^\d{12}$', cccd):
            messages.error(request, "CCCD không hợp lệ. Vui lòng nhập 12 chữ số.")
            return redirect('service')
        try:
            # Tạo thành viên mới
            FamilyMember.objects.create(
                room_id=room_user.room_id,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=dob,
                cccd=cccd,
                email=email,
                phone_number=phone_number
            )
            messages.success(request, "Thêm thành viên thành công.")
        except IntegrityError:
            # Xử lý lỗi UNIQUE constraint liên quan đến CCCD hoặc các trường khác
            messages.error(request, "Thông tin thành viên không hợp lệ. CCCD đã tồn tại.")
        except Exception as e:
            # Xử lý các lỗi không mong muốn khác
            messages.error(request, f"Đã xảy ra lỗi: {str(e)}")

        return redirect('service')

    return render(request, 'app/add_member.html')


@login_required
def wait(request):
    form = CustomAuthenticationForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        if user.is_approved:
            login(request, user)
            return redirect('homepage')
    return redirect('homepage')

@login_required
def service_view(request):
    user = request.user
    family_group = Group.objects.filter(user=user).first()  # Lấy group đầu tiên mà user thuộc
    is_member = family_group is not None
    return render(request, 'app/service.html', {'is_member': is_member})
