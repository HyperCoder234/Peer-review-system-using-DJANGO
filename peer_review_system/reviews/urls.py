from django.urls import path
from .views import home, list_reviews, add_review, upload_assignment, assignment_list, delete_assignment, logout_view
from django.contrib.auth.views import LoginView

app_name = "reviews"

urlpatterns = [
    path('', home, name='home'),
    path('reviews/', list_reviews, name='list_reviews'),
    path('reviews/add/', add_review, name='add_review'),

    path('assignments/', assignment_list, name='assignment_list'),
    path('assignments/upload/', upload_assignment, name='upload_assignment'),
    path('assignments/delete/<int:assignment_id>/', delete_assignment, name='delete_assignment'),

    path('login/', LoginView.as_view(template_name='reviews/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),  # ✅ Custom Logout View
]
