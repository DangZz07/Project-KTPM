# phần admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Payment, Charge, FamilyMember, Article, RoomUser, SuperUser,apartment, Vehicle, Notification
from .forms import ChargeForm, PaymentForm, NotificationForm
from . import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
admin.site.site_header = "Chung cư Blue Moon"
admin.site.site_title = "Quản lý chung cư"
admin.site.index_title = "Các chức năng"

# Register the Article model
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = forms.ArticleForm
    list_display = ('title', 'content', 'date')
    search_fields = ('title', 'content')
    list_filter = ('date',)
    readonly_fields = ('date',)# Bộ lọc theo ngày
    #Thêm file CSS
    class Media:
        css = {
            'all': ('css/custom_admin.css',) 
        }
    # Tùy chỉnh title
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = _("Quản lý thông báo")
        return super().changelist_view(request, extra_context=extra_context)
    # Tắt các nút "Lưu và thêm mới" và "Lưu và tiếp tục chỉnh sửa" mặc định của Django
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().changeform_view(request, object_id, form_url, extra_context)
# admin.site.register(Article, ArticleAdmin)

#Quản lí tài khoản người dùng
@admin.register(RoomUser)
class RoomUser(admin.ModelAdmin):
    form = forms.RoomUserForm
    list_display = ['username', 'room_id', 'registry_email','phone_number','is_approved']
    search_fields = ['username', 'room_id__room_id', 'registry_email','phone_number','is_approved']
    exclude = ['last_login','password', 'is_active']
    class Media:
        css = {
            'all': ('css/custom_admin.css',)  
        }
    # Tùy chỉnh title
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = _("Quản lý tài khoản")
        return super().changelist_view(request, extra_context=extra_context)
    # Tắt các nút "Lưu và thêm mới" và "Lưu và tiếp tục chỉnh sửa" mặc định của Django
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().changeform_view(request, object_id, form_url, extra_context)
    

#Quản lí phương tiện
@admin.register(Vehicle)
class VehicleIn4(admin.ModelAdmin):
    list_display = ('room_id', 'license_plate', 'type_vehicle')
    search_fields = ('license_plate', 'type_vehicle', 'room_id__room_id')
    list_filter = ('type_vehicle','room_id')
    class Media:
        css = {
            'all': ('css/custom_admin.css',)
        }
    # Tùy chỉnh title
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = _("Quản lý gửi xe")
        return super().changelist_view(request, extra_context=extra_context)
    # Tắt các nút "Lưu và thêm mới" và "Lưu và tiếp tục chỉnh sửa" mặc định của Django
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().changeform_view(request, object_id, form_url, extra_context)
# admin.site.register(Vehicle,VehicleIn4)

#Quản lí khoản thanh toán  
@admin.register(Payment)
class PaymentIn4(admin.ModelAdmin):
    form = PaymentForm
    list_display = ('get_charge_name','room_id', 'amount', 'date', 'status')
    search_fields = ('room_id__room_id', 'charge_id__name', 'status')
    list_filter = ('status', 'charge_id__name', 'room_id')
    # readonly_fields = ('charge_id','room_id', 'amount', 'date')
    readonly_fields = ['date']

    fieldsets = (
        (None, { 
            'fields': ('charge_id','room_id', 'amount', 'date', 'status'),
        }),
    )
    class Media:
        css = {
            'all': ('css/custom_admin.css',)  # Custom CSS for admin panel
        }

    # Customizing the title of the changelist view
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = _("Quản lý thanh toán")  # Translatable title
        return super().changelist_view(request, extra_context=extra_context)

    # Custom display for "charge name" with a column label
    @admin.display(description=_('Tên khoản thu'))  # Translatable column label
    def get_charge_name(self, obj):
        return obj.charge_id.name if obj.charge_id else "N/A"

    # # Custom display for "status" with a column label
    # @admin.display(description=_('Trạng thái'))  # Translatable column label
    # def display_status(self, obj):
    #     return _("Đã thanh toán") if obj.status else _("Chưa thanh toán")

    # Customizing the change form view to hide default save buttons
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False  # Disable "Save and add another"
        extra_context['show_save_and_continue'] = False  # Disable "Save and continue editing"
        extra_context['show_delete'] = False  # Disable "Delete" button
        return super().changeform_view(request, object_id, form_url, extra_context)
    
# admin.site.register(Payment,PaymentIn4)

#Quản lí nhân khẩu
@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    form = forms.FamilyMemberForm
    list_display = ('room_id', 'first_name', 'last_name', 'date_of_birth','cccd', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    list_filter = ('room_id',)
    class Media:
        css = {
            'all': ('css/custom_admin.css',) 
        }
    # Tùy chỉnh title
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = _("Quản lý nhân khẩu")
        return super().changelist_view(request, extra_context=extra_context)
    # Tắt các nút "Lưu và thêm mới" và "Lưu và tiếp tục chỉnh sửa" mặc định của Django
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().changeform_view(request, object_id, form_url, extra_context)
    # chia fieldset thành các nhóm
    fieldsets = (
        ('Thông tin cá nhân', {
            'fields': ('room_id', 'first_name', 'last_name', 'date_of_birth','cccd')
        }),
        ('Thông tin liên hệ', {
            'fields': ('email', 'phone_number')
        }),
    )

# Register the custom admin class with the FamilyMember model
# admin.site.register(FamilyMember, FamilyMemberAdmin)


#Quản lí thông báo
@admin.register(Notification)
class NotiIn4(admin.ModelAdmin):
    form = NotificationForm
    list_display = ('title', 'content', 'room_id')
    search_fields = ('title','room_id__room_id')
    list_filter = ('date','room_id')
    class Media:
        css = {
            'all': ('css/custom_admin.css',) 
        }
   
    # Tùy chỉnh title
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = _("Quản lý thông báo")
        return super().changelist_view(request, extra_context=extra_context)
    # Tắt các nút "Lưu và thêm mới" và "Lưu và tiếp tục chỉnh sửa" mặc định của Django
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().changeform_view(request, object_id, form_url, extra_context)
# admin.site.register(Notification,NotiIn4)

#Quan li khoản thu
@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    form = ChargeForm
    list_display = ('category', 'name', 'create_at', 'create_by', 'deadline', 'get_payment_summary')
    search_fields = ('name', 'category', 'create_by__username')
    list_filter = ('category', 'create_at', 'deadline')
    
    @admin.display(description='Số phòng đã nộp')
    def get_payment_summary(self, obj):
        return obj.get_payment_summary()
    
    class Media:
        css = {
            'all': ('css/custom_admin.css',)  
        }
    # tạo title cho header
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = _("Quản lý khoản thu")
        return super().changelist_view(request, extra_context=extra_context)
    # Tắt các nút "Lưu và thêm mới" và "Lưu và tiếp tục chỉnh sửa" mặc định của Django
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().changeform_view(request, object_id, form_url, extra_context)
    
    # lưu khoản thu vào DB
    def save_model(self, request, obj, form, change):
        # Lưu khoản thu  trước
        if not change:  # Khi thêm mới
            obj.create_by = request.user  # Gán người tạo là admin đang đăng nhập
        super().save_model(request, obj, form, change)


        category = form.cleaned_data.get("category")
        excel_file = form.cleaned_data.get("excel_file")
        unit_price = form.cleaned_data.get("unit_price")

        if category in ["Tiền điện", "Tiền nước"] and excel_file:
            # Xử lý file Excel
            try:
                target_residents = form.process_excel_file(excel_file, obj)
                # Thêm các target_room vào charge
                obj.target_room.set(target_residents)
                obj.save()
            except ValidationError as e:
                raise ValidationError(f"Lỗi khi xử lý file Excel: {e}")
        elif category in ["Phí dịch vụ", "Phí quản lý"] and unit_price:
            # Tính toán amount từ đơn giá
            form.calculate_service_fee(unit_price, obj)
            # Thêm các target_room vào charge (chỉ phòng có người ở)
            from .models import RoomUser
            active_room_ids = RoomUser.objects.filter(is_active=True).values_list('room_id', flat=True).distinct()
            target_residents = apartment.objects.filter(room_id__in=active_room_ids)
            obj.target_room.set(target_residents)
            obj.save()
        elif category == "Phí gửi xe":
            form.calculate_parking_fee(obj)
            # Thêm các target_room vào charge
            target_residents = Vehicle.objects.values_list('room_id', flat=True).distinct()
            obj.target_room.set(target_residents)
            obj.save()
            
            
# admin.site.register(Charge,ChargeAdmin)