from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.timezone import now

# 📌 Helper Functions for Organized File Upload Paths
def assignment_upload_path(instance, filename):
    return f"assignments/user_{instance.uploader.id}/{filename}"

def submission_upload_path(instance, filename):
    return f"submissions/user_{instance.student.id}/{filename}"


# 📌 Review Model (For Peer Reviews)
class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="given_reviews")
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_reviews")
    feedback = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer.username} → {self.reviewee.username} ({self.rating}/5)"

    def clean(self):
        if not (1 <= self.rating <= 5):
            raise ValidationError("❌ Rating must be between 1 and 5.")


# 📌 Assignment Model (For Uploading Assignments)
class Assignment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)  # Optional Description
    file = models.FileField(upload_to=assignment_upload_path)  # File Upload Path
    due_date = models.DateTimeField(null=True, blank=True)  # ✅ NULL Allowed
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assignments")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.title} ({self.status}) by {self.uploader.username}"

    def is_past_due(self):
        """Check if the assignment's due date is passed."""
        return self.due_date and now() > self.due_date

    def clean(self):
        """Ensure that due_date is in the future while creating an assignment."""
        if self.due_date and self.due_date < now():
            raise ValidationError("❌ Due date cannot be in the past.")


# 📌 Submission Model (For Student Submissions)
class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    file = models.FileField(upload_to=submission_upload_path)  # File Upload Path
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_late = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Automatically mark submission as late if submitted after due date."""
        if self.assignment.due_date and now() > self.assignment.due_date:
            self.is_late = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.username} → {self.assignment.title} ({'Late' if self.is_late else 'On Time'})"
