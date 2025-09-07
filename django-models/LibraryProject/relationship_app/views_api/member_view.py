from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(is_member)
def member_dashboard(request):
    return render(request, 'member_view.html')