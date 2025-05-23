from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            user.last_online = now()
            user.save(update_fields=['last_online'])
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None