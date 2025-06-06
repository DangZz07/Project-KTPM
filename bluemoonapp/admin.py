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
admin.site.register(Article, ArticleAdmin)

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