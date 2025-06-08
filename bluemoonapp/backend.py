from django.contrib.auth.backends import BaseBackend
from .models import RoomUser, SuperUser

class MultiUserModelBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Check RoomUser model
        try:
            room_user = RoomUser.objects.get(username=username)
            if room_user.check_password(password) and room_user.is_active:
                return room_user
        except RoomUser.DoesNotExist:
            pass

        # Check SuperUser model
        # try:
        #     super_user = SuperUser.objects.get(username=username)
        #     if super_user.check_password(password) and super_user.is_active:
        #         return super_user
        # except SuperUser.DoesNotExist:
        #     pass

        # return None

    def get_user(self, user_id):
        # Check both RoomUser and SuperUser models for the user ID
        try:
            return RoomUser.objects.get(pk=user_id)
        except RoomUser.DoesNotExist:
            pass

        # try:
        #     return SuperUser.objects.get(pk=user_id)
        # except SuperUser.DoesNotExist:
        #     return None
