from django import forms
from django.utils.translation import gettext_lazy as _

class RiddleAnswerForm(forms.Form):

    answer = forms.CharField(required=True,
                             help_text=_("Your answer"))

    # def clean(self):
    #     cleaned_data = super().clean()
    #     answer = cleaned_data.get("answer")
    #     return answer.strip().upper() == a2.strip().upper()
