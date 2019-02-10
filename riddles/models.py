from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import uuid

class Riddle(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(null=False, blank=False)
    title = models.CharField(max_length=30, null=False, blank=False)
    answer = models.CharField(max_length=30, null=True, blank=True)
    next = models.ForeignKey("Riddle", blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    @property
    def is_final(self):
        return not self.next and not self.answer

    def get_absolute_url(self):
        return reverse("riddle-detail", kwargs={"pk": self.id})

    def clean(self):
        if (self.next is None and self.answer is not None) or (self.next is not None and self.answer is None):
            raise ValidationError(_("Either next and answer are defined or not."))

    class Meta:
        ordering = ["title",]
