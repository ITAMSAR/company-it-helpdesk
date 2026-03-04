from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def logout_view(request):
    """Custom logout view that handles both GET and POST"""
    if request.method == 'POST':
        # Logout user
        logout(request)
        return render(request, 'logout.html')
    else:
        # Show confirmation page
        return render(request, 'logout_confirm.html')
