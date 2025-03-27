import os
from django import forms
from .models import Review, Assignment

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewee', 'feedback', 'rating']

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not (1 <= rating <= 5):
            raise forms.ValidationError("❌ Rating must be between 1 and 5.")
        return rating


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'file', 'due_date']

    def clean_file(self):
        file = self.cleaned_data.get('file')

        # ✅ Step 1: Check if file exists
        if not file:
            raise forms.ValidationError("❌ File is required for submission.")

        # ✅ Step 2: Check file size (Max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if file.size > max_size:
            raise forms.ValidationError(f"❌ File size should not exceed {max_size / (1024 * 1024)}MB.")

        # ✅ Step 3: Check allowed file formats
        allowed_extensions = ['.pdf', '.ppt', '.pptx', '.doc', '.docx', '.jpg', '.jpeg', '.png']
        ext = os.path.splitext(file.name)[1].lower()

        if ext not in allowed_extensions:
            raise forms.ValidationError(f"❌ Unsupported file format. Allowed: {', '.join(allowed_extensions)}")

        return file
