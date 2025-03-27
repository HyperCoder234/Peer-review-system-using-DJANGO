from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from reviews import views  # 👈 Reviews app ke views import kar rahe hain
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reviews/', include('reviews.urls')),  # 👈 Reviews app ke URLs include kiye
    path('', views.home, name='home'),  # 👈 Home Page Route
    path('accounts/', include('django.contrib.auth.urls')),  # ✅ Built-in auth URLs
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # ✅ Fixed Logout Redirect
]

# ✅ Static aur Media Files Serve Karne ke liye
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
elif settings.MEDIA_URL and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # ✅ Deployment ke liye media serve fix
