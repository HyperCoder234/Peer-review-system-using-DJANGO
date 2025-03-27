from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Review, Assignment
from .forms import ReviewForm

# ======================== MODEL TESTS ========================
class ReviewModelTest(TestCase):
    def setUp(self):
        """Create test users and a review before each test"""
        self.reviewer = User.objects.create_user(username="reviewer", password="testpass")
        self.reviewee = User.objects.create_user(username="reviewee", password="testpass")
        self.review = Review.objects.create(
            reviewer=self.reviewer,
            reviewee=self.reviewee,
            feedback="Great work!",
            rating=5
        )

    def test_review_content(self):
        """Check if the review content is stored correctly"""
        self.assertEqual(self.review.feedback, "Great work!")
        self.assertEqual(self.review.rating, 5)

    def test_review_str(self):
        """Check the string representation of Review model"""
        self.assertEqual(str(self.review), "reviewer → reviewee (5/5)")


# ======================== FORM TESTS ========================
class ReviewFormTest(TestCase):
    def test_valid_review_form(self):
        """Test a valid review form"""
        user = User.objects.create_user(username="testuser", password="testpass")
        form_data = {"reviewee": user.id, "feedback": "Awesome job!", "rating": 4}
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())  # Form should be valid

    def test_invalid_review_form(self):
        """Test an invalid review form (missing feedback)"""
        user = User.objects.create_user(username="testuser", password="testpass")
        form_data = {"reviewee": user.id, "rating": 4}
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())  # Feedback field is required


# ======================== VIEW TESTS ========================
class ReviewViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_review_page_redirect_if_not_logged_in(self):
        """Check if review page redirects unauthenticated users"""
        response = self.client.get(reverse("reviews:review_page"))  # Use correct URL name with namespace
        self.assertEqual(response.status_code, 302)  # 302 means redirect (to login page)

    def test_review_page_load_for_logged_in_user(self):
        """Check if review page loads for logged-in users"""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("reviews:review_page"))  # Use correct URL name with namespace
        self.assertEqual(response.status_code, 200)  # 200 means success


# ======================== ASSIGNMENT UPLOAD TESTS ========================
class AssignmentUploadTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_assignment_upload(self):
        """Test uploading assignment successfully"""
        self.client.login(username="testuser", password="testpass")
        file = open('path/to/sample/file.pdf', 'rb')  # Test file for assignment upload
        response = self.client.post(reverse("reviews:upload_assignment"), {
            "title": "Test Assignment",
            "description": "Test Assignment Description",
            "file": file,
            "due_date": "2025-12-12 10:00:00"
        })
        file.close()  # Don't forget to close the file!
        self.assertEqual(response.status_code, 302)  # 302 means redirect after successful upload

    def test_invalid_assignment_upload(self):
        """Test invalid assignment upload (missing due_date)"""
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("reviews:upload_assignment"), {
            "title": "Test Assignment",
            "description": "Test Assignment Description",
            # Missing file and due_date
        })
        self.assertEqual(response.status_code, 200)  # Should return 200 for failed upload
        self.assertFormError(response, "form", "due_date", "This field is required.")  # Expecting error for missing due_date
