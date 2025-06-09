# Description: Script để tạo dữ liệu mẫu trong database

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from nmcnpmapp.models import apartment
# Tạo dữ liệu mẫu cho bảng apartment
def populate_apartments():
    apartments = []
    for floor in range(1, 10):  # Tầng từ 1 đến 9
        for room in range(1, 21):  # Mỗi tầng có 20 phòng
            room_id = int(f"{floor}{room:02d}")
            area = 40 if room <= 9 else 60 if 9 < room <= 15 else 80
            apartments.append(apartment(room_id=room_id, area=area))

    apartment.objects.bulk_create(apartments, ignore_conflicts=True)
    print(f"Created {len(apartments)} apartments!")

if __name__ == "__main__":
    populate_apartments()

# class YourAppConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'nmcnpmapp'

#     def ready(self):
#         from .models import apartment
#         from django.db import connections

#         def populate_apartments(sender, **kwargs):
#             # Kiểm tra chỉ khởi tạo khi bảng chưa có dữ liệu
#             if not apartment.objects.exists():
#                 apartments = []
#                 for floor in range(1, 21):  # Tầng từ 1 đến 20
#                     for room in range(1, 15):  # Mỗi tầng có 14 phòng
#                         room_id = int(f"{floor}{room:02d}")
#                         area = 40 if room <= 9 else 60 if 9 < room <= 12 else 80
#                         apartments.append(apartment(room_id=room_id, area=area))

#                 apartment.objects.bulk_create(apartments)
#                 print(f"Created {len(apartments)} apartments.")
#         def populate_family_members(sender, **kwargs):
#             # Kiểm tra và thêm dữ liệu cho FamilyMember
#             if not FamilyMember.objects.exists():
#                 first_names = ["Kiệt", "An", "Minh", "Vinh", "Tuấn", "Phúc", "Long", "Huy", "Hùng", "Hải", "Thành", "Hà", "Hoa", "Hương", "Linh", "Thảo", "Trang", "Trâm", "Thu", "Thủy", "Thúy", "Tuyết", "Tâm", "Tú", "Tùng"]
#                 last_names = ["Nguyễn", "Trần", "Lê", "Phùng", "Nguyễn LuLu"]
#                 emails = ["example@gmail.com", "test@gmail.com", "user@gmail.com"]
#                 phone_prefix = "0123"

#                 family_members = []
#                 for apartment_instance in apartment.objects.all():
#                     # Mỗi phòng có từ 3 đến 5 thành viên
#                     num_members = random.randint(3, 5)
#                     for _ in range(num_members):
#                         first_name = random.choice(first_names)
#                         last_name = random.choice(last_names)
#                         email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(emails)}"
#                         phone_number = f"{phone_prefix}{random.randint(1000000, 9999999)}"
#                         date_of_birth = f"19{random.randint(70, 99)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"  # Random DOB

#                         family_members.append(
#                             FamilyMember(
#                                 room_id=apartment_instance,
#                                 first_name=first_name,
#                                 last_name=last_name,
#                                 email=email,
#                                 phone_number=phone_number,
#                                 dateofbirth=date_of_birth,
#                             )
#                         )

#                 FamilyMember.objects.bulk_create(family_members)
#                 print(f"Created {len(family_members)} family members.")

#         post_migrate.connect(populate_apartments, sender=self)