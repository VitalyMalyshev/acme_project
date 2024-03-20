from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown, get_birthday_for_year
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView,
)    
from django.urls import reverse_lazy


class BirthdayMixin:
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayFormMixin:
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html' # либо переименовать шаблон в birthday_form.html и удалить


class BirthdayCreateView(BirthdayMixin, BirthdayFormMixin, CreateView):
    pass


class BirthdayUpdateView(BirthdayMixin, BirthdayFormMixin, UpdateView):
    pass


class BirthdayDeleteView(BirthdayMixin, DeleteView):
    pass 


class BirthdayListView(BirthdayMixin, ListView):
    ordering = 'id'
    paginate_by = 10


# Новый класс
class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['birthday_countdown'] = calculate_birthday_countdown(
            # Дату рождения берём из объекта в словаре context:
            self.object.birthday
        )
        # Возвращаем словарь контекста.
        return context
