from kivy.utils import platform
from PIL import ImageOps


def is_android():
    return platform == 'android'


def is_ios():
    return platform == 'ios'


def check_camera_permission():
    """
    Android runtime `CAMERA` permission check.
    """
    if not is_android():
        return True
    from android.permissions import Permission, check_permission
    permission = Permission.CAMERA
    return check_permission(permission)


def check_request_camera_permission(callback=None):
    """
    Android runtime `CAMERA` permission check & request.
    """
    had_permission = check_camera_permission()
    if not had_permission:
        from android.permissions import Permission, request_permissions
        permissions = [Permission.CAMERA]
        request_permissions(permissions, callback)
    return had_permission


def fix_android_image(pil_image):
    """
    On Android, the image seems mirrored and rotated somehow, refs #32.
    """
    if not is_android():
        return pil_image
    pil_image = pil_image.rotate(90)
    pil_image = ImageOps.mirror(pil_image)
    return pil_image
