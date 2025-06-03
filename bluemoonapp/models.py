#models.py
# =========================
# Các model quản lý hệ thống chung cư: tài khoản, phòng, phương tiện, khoản thu, thanh toán, nhân khẩu, thông báo
# =========================

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models

# =========================
# 1. Quản lý tài khoản phòng (RoomUser, SuperUser)
# =========================

class RoomUserManager(BaseUserManager):
    """
    Custom manager cho RoomUser, dùng để tạo user mới với các trường bắt buộc.
    """
    def create_user(self, room_id, username, registry_email, password=None, **extra_fields):
        # Kiểm tra các trường bắt buộc
        if not room_id:
            raise ValueError("The Room ID field must be set.")
        if not username:
            raise ValueError("The Username field must be set.")
        if not registry_email:
            raise ValueError("The Email field must be set.")
        # Chuẩn hóa email và username
        registry_email = self.normalize_email(registry_email)
        username = self.model.normalize_username(username)
        # Kiểm tra trùng username/email
        if RoomUser.objects.filter(username=username).exists():
            raise ValueError("A user with this Username already exists.")
        if RoomUser.objects.filter(registry_email=registry_email).exists():
            raise ValueError("A user with this Email already exists.")
        # Tạo user
        extra_fields.setdefault('is_active', True)
        user = self.model(
            room_id=room_id,
            username=username,
            registry_email=registry_email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class SuperUserManager(BaseUserManager):
    """
    Custom manager cho SuperUser (admin hệ thống).
    """
    def create_superuser(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class SuperUser(AbstractBaseUser, PermissionsMixin):
    """
    Model cho tài khoản quản trị hệ thống (admin).
    """
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    # The is_superuser field is inherited from PermissionsMixin
    objects = SuperUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    def __str__(self):
        return self.username
    
class apartment(models.Model):
    """
    Model đại diện cho một phòng/căn hộ trong chung cư.
    """
    room_id = models.IntegerField(primary_key=True)  # Mã phòng (duy nhất)
    area = models.IntegerField(default =0)           # Diện tích phòng (m2)
    def __str__(self) -> str:
        return f"Phòng {self.room_id}"

class RoomUser(AbstractBaseUser):
    """
    Model cho tài khoản người dùng đại diện cho từng phòng.
    - Mỗi RoomUser gắn với một apartment (phòng).
    """
    room_id = models.ForeignKey(apartment, on_delete=models.CASCADE,related_name="user",verbose_name="Số phòng")
    username = models.CharField(max_length=100, unique=True,verbose_name="Tên tài khoản")
    registry_email = models.EmailField(default="example@gmail.com",verbose_name="Email")
    phone_number = models.CharField(max_length=10, unique=True,verbose_name="Số điện thoại")
    is_approved = models.BooleanField(max_length=10,choices=[(False,"Chưa duyệt"),(True,"Đã duyệt")],default=False,verbose_name="Trạng thái duyệt")
    is_active = models.BooleanField(default=True,verbose_name="Tài khoản hoạt động")
    objects = RoomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['room_id', 'registry_email', 'phone_number']
    def __str__(self):
        return self.username
    class Meta:
        verbose_name = "Tài khoản"
        verbose_name_plural = "Quản lý tài khoản"

# =========================
# 2. Quản lý phương tiện gửi xe
# =========================

class Vehicle(models.Model):
    """
    Model cho phương tiện gửi xe của từng phòng.
    - Mỗi phương tiện gắn với một phòng.
    """
    CATEGORY_CHOICES = [
        (1, "Xe đạp"),
        (2, "Xe máy"),
        (3, "Ô tô"),
    ]
    license_plate = models.CharField(max_length=30,verbose_name="Biển số xe")
    type_vehicle = models.IntegerField(choices=CATEGORY_CHOICES,verbose_name="Loại xe")
    room_id = models.ForeignKey(apartment, on_delete=models.CASCADE, related_name="vehicles",verbose_name='Số phòng')
    class Meta:
        verbose_name = "Thông tin gửi xe"
        verbose_name_plural = "Quản lý gửi xe"
    
# =========================
# 3. Quản lý khoản thu và thanh toán
# =========================

class Charge(models.Model):
    """
    Model cho các khoản thu (phí dịch vụ, điện, nước, gửi xe, ...).
    - target_room: các phòng phải đóng khoản này (ManyToMany).
    """
    CATEGORY_CHOICES = [
    ("Tiền điện", "Tiền điện"),
    ("Tiền nước", "Tiền nước"),
    ("Phí dịch vụ", "Phí dịch vụ"),
    ("Phí quản lý", "Phí quản lý"),
    ("Phí gửi xe", "Phí gửi xe"),
    ("Khác", "Khác"),
    ]
    charge_id = models.AutoField(primary_key=True,verbose_name="Mã khoản thu")
    name = models.CharField(max_length=255,verbose_name="Tên khoản thu")
    create_at = models.DateField(auto_now_add=True,verbose_name="Ngày tạo")
    create_by = models.ForeignKey(SuperUser,on_delete = models.CASCADE, related_name="charges",verbose_name="Người tạo")
    deadline = models.DateField(verbose_name="Hạn thanh toán")
    target_room = models.ManyToManyField(apartment, related_name="charges",verbose_name="Đối tượng thu")  # Các phòng phải đóng khoản này
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="Khác",verbose_name="Loại khoản thu")
    def __str__(self):
        return self.name
    def get_payment_summary(self):
        """
        Trả về chuỗi "số phòng đã đóng / tổng số phòng phải đóng" cho khoản thu này.
        """
        total_rooms = self.target_room.count()
        paid_rooms = self.payments.filter(status=True).values_list('room_id', flat=True).distinct().count()
        return f"{paid_rooms} / {total_rooms}"
    class Meta:
        verbose_name = "Khoản thu"
        verbose_name_plural = "Quản lý khoản thu"

class Payment(models.Model):
    """
    Model cho từng lần thanh toán của một phòng cho một khoản thu.
    - Mỗi payment gắn với một Charge và một apartment.
    """
    payment_id = models.AutoField(primary_key=True,verbose_name="Mã thanh toán")
    charge_id = models.ForeignKey(Charge, on_delete=models.CASCADE, related_name="payments",verbose_name="Mã khoản thu")
    room_id = models.ForeignKey(apartment, on_delete=models.CASCADE, related_name="payments",verbose_name="Số phòng")
    amount = models.PositiveIntegerField(verbose_name="Số tiền")
    date = models.DateField(auto_now_add=True,verbose_name="Ngày tạo")
    status = models.BooleanField(default=False,verbose_name="Trạng thái")  # True: đã đóng, False: chưa đóng
    class Meta:
        verbose_name = "Khoản thanh toán"
        verbose_name_plural = "Quản lý khoản thanh toán"
    def __str__(self):
        return f"Mã thanh toán {self.payment_id}"

# =========================
# 4. Quản lý nhân khẩu (thành viên trong phòng)
# =========================

class FamilyMember(models.Model):
    """
    Model cho từng thành viên trong một phòng/căn hộ.
    """
    id = models.AutoField(primary_key=True)
    room_id = models.ForeignKey(apartment, on_delete=models.CASCADE, related_name="family_members",verbose_name="Số phòng")
    first_name = models.CharField(max_length=50,verbose_name="Họ")
    last_name = models.CharField(max_length=50,verbose_name="Tên")
    date_of_birth = models.DateField(null=True, blank=True,verbose_name="Ngày sinh")
    cccd = models.CharField(
        max_length=12, 
        unique=True, 
        default="106872712222", 
        verbose_name="Số CCCD"
    )
    email = models.EmailField(default="lol@gmail.com")
    phone_number = models.CharField(max_length=10, default="0123456789",verbose_name="Số điện thoại")
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    class Meta:
        verbose_name = "Nhân khẩu"
        verbose_name_plural = "Quản lý nhân khẩu"

# =========================
# 5. Quản lý thông báo
# =========================

class Article(models.Model):
    """
    Model cho các bài viết/thông báo chung.
    """
    title = models.CharField(max_length=255,verbose_name="Tiêu đề")
    content = models.TextField(verbose_name="Nội dung")
    date = models.DateField(auto_now_add=True,verbose_name="Ngày đăng")
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Thông báo"
        verbose_name_plural = "Quản lý thông báo"
