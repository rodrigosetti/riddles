from .models import Riddle
from .forms import RiddleAnswerForm
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import FormView
from django.urls import reverse
from django.views import View
from django.contrib import messages

def compare_answer(a1, a2):
    return a1.strip().upper() == a2.strip().upper()

class RiddleDisplay(DetailView):
    model = Riddle

    def get(self, request, *args, **kwargs):
        last_riddle_id = request.session.get("last_riddle_id")
        if last_riddle_id is not None and last_riddle_id != str(self.get_object().id):
            messages.info(request, _("Looking for the <a href='%(url)s'>last riddle you attempted?</a>") %
                          {"url": reverse("riddle-detail", kwargs={"pk": last_riddle_id})})
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RiddleAnswerForm()
        return context

class RiddleAnswer(SingleObjectMixin, FormView):
    model = Riddle
    form_class = RiddleAnswerForm
    template_name = "riddles/riddle_detail.html"

    def form_valid(self, form):
        if not compare_answer(form.cleaned_data["answer"], self.object.answer):
            form.add_error("answer", ValidationError(_("Incorrect answer")))
            return self.form_invalid(form)
        else:
            self.request.session["last_riddle_id"] = str(self.object.next_id)
            return super().form_valid(form)

    def get_success_url(self):
        return reverse("riddle-detail", kwargs={"pk": self.object.next.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

class RiddleDetail(View):

    def get(self, request, *args, **kwargs):
        view = RiddleDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = RiddleAnswer.as_view()
        return view(request, *args, **kwargs)
