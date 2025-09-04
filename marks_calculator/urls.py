
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),   # gives /login, /logout, /register
    path('marks/', include('marks.urls')),
    path('', root_redirect),              # root → login or dashboard
]
