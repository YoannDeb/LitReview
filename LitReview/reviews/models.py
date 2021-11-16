from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

from django_resized import ResizedImageField


class Ticket(models.Model):
    """
    Ticket model class, child of Model django's generic class.
    Image is automatically resized using django_resized module.
    """
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    image = ResizedImageField(size=[200, 300], quality=100, force_format='JPEG', null=True, blank=True, upload_to='book_covers')
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    """
    Review model class, child of Model django's generic class.
    Rating uses validators to ensure it is between 0 and 5.
    """
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.headline


class UserFollow(models.Model):
    """
    User follow model class, child of Model django's generic class.
    Subclass Meta ensures we don't get multiple UserFollows instances for unique user-user_followed pairs.
    """
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following'
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by'
    )

    def __str__(self):
        return f"{self.user.username} abonné à {self.followed_user.username}"

    class Meta:
        unique_together = ('user', 'followed_user', )
        verbose_name = _("Abonné à un utilisateur")
        verbose_name_plural = _("Abonnés aux utilisateurs")

