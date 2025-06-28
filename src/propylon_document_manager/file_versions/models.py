from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager as BaseUserManager
from django.db.models import CharField, EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

#need this to bypass username error
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
class User(AbstractUser):
    """
    Default custom user model for Propylon Document Manager.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

class ContentBlob(models.Model):
    """Content Addressable Storage mechanism."""
    content_hash = models.CharField(max_length=64)  # SHA-256
    data = models.BinaryField()  # FileField for large files
    size = models.PositiveIntegerField()  # bytes
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "CAS Content Blob"

class File(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    url_path = models.CharField(max_length=1024)  # e.g. "/documents/reviews/review.pdf"
    created_at = models.DateTimeField(auto_now_add=True)
    
    #might need this
    # current_version_id = models.PositiveIntegerField(null=True)
    # @property
    # def current_version(self):
    #     return self.versions.filter(version_number=self.current_version_id).first()

class FileVersion(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField()
    file_name = models.CharField(max_length=512)  
    content_blob = models.ForeignKey(ContentBlob, on_delete=models.PROTECT)  # CAS reference
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_latest = models.BooleanField(default=True)

    class Meta:
        unique_together = [('file', 'version_number')]
        ordering = ['-version_number']