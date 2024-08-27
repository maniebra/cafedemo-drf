from .models import User


def get_current_user(request):
    return User.objects.filter(id=request.user.id).first()


def is_current_user_admin(request):
    return get_current_user(request).is_admin
