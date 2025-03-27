from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from .models import Review, Assignment
from .forms import ReviewForm, AssignmentForm
import logging

# ✅ Logger Setup (Debugging ke liye)
logger = logging.getLogger(__name__)

# ✅ Home Page
def home(request):
    return render(request, 'reviews/home.html')

# ✅ List Reviews
@login_required
def list_reviews(request):
    reviews = Review.objects.select_related("reviewer", "reviewee").all()
    return render(request, 'reviews/list_reviews.html', {'reviews': reviews})

# ✅ Add Review
@login_required
def add_review(request):
    form = ReviewForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.save()
            messages.success(request, "✅ Review added successfully!")
            return redirect('reviews:list_reviews')  # ✅ Fixed Namespace Issue
        else:
            messages.error(request, "❌ Please fix the errors below.")
            logger.error("Review submission failed: %s", form.errors)

    return render(request, 'reviews/add_review.html', {'form': form})

# ✅ Upload Assignment
@login_required
def upload_assignment(request):
    form = AssignmentForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.uploader = request.user  
            assignment.save()
            messages.success(request, "✅ Assignment uploaded successfully!")
            return redirect('reviews:assignment_list')  # ✅ Fixed Namespace Issue
        else:
            messages.error(request, "❌ Failed to upload. Please check the form.")
            logger.error("Assignment upload failed: %s", form.errors)

    return render(request, 'reviews/upload_assignment.html', {'form': form})

# ✅ Assignment List
@login_required
def assignment_list(request):
    assignments = Assignment.objects.select_related("uploader").all()
    return render(request, 'reviews/assignment_list.html', {'assignments': assignments})

# ✅ Delete Assignment
@login_required
def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    # ✅ Ensure only uploader or admin can delete
    if request.user != assignment.uploader and not request.user.is_superuser:
        messages.error(request, "❌ You are not authorized to delete this assignment.")
        return redirect('reviews:assignment_list')

    if request.method == "POST":
        assignment.delete()
        messages.success(request, "✅ Assignment deleted successfully!")
        return redirect('reviews:assignment_list')

    return render(request, 'reviews/confirm_delete.html', {'assignment': assignment})

# ✅ Logout View (Fixed Redirect)
@login_required
def logout_view(request):
    if request.method == "POST":  # ✅ Only POST request allowed
        logout(request)
        return redirect("reviews:login")  # ✅ Logout hone ke baad login page pe jayega
    return redirect("reviews:home")  # ❌ GET request allowed nahi hai, home pe redirect hoga
