from .models import User
from django.core.exceptions import ObjectDoesNotExist

def userprofile_context(request):
  if request.user.is_authenticated:
    try:
      userprofile = User.objects.get(id=request.user.id)
      return {'userprofile': userprofile}
    except ObjectDoesNotExist:
      pass
  return {}
