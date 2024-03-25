# birthday/views.py
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)
from django.urls import reverse_lazy
from .forms import BirthdayForm
from .models import Birthday, Congratulation
from .utils import calculate_birthday_countdown
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
# Или вместо 404 можно импортируем ошибку доступа - 
# для показа юзеру при попытке отредактировать не свой пост:
# from django.core.exceptions import PermissionDenied

# А следующие импорты нужны именно для поздравлений:
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .forms import CongratulationForm


class BirthdayListView(ListView):
    model = Birthday
    ordering = 'id'
    paginate_by = 10


class BirthdayCreateView(LoginRequiredMixin, CreateView):
    model = Birthday
    form_class = BirthdayForm

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)


class BirthdayUpdateView(LoginRequiredMixin, UpdateView):
    model = Birthday
    form_class = BirthdayForm
    # При работе с CBV для выполнения этой проверки нужно переопределить метод dispatch(),
    # который работает как диспетчер, перенаправляя запросы согласно их HTTP-методам:
    # GET-запрос к методу CBV get(), POST-запрос к методу post() и так далее.
    # Если пользователь, выполняющий запрос, не является автором объекта, то и пускать его дальше не надо:
    def dispatch(self, request, *args, **kwargs):
        # Получаем объект по первичному ключу и автору или вызываем 404 ошибку.
        get_object_or_404(Birthday, pk=kwargs['pk'], author=request.user)
        # Если объект был найден, то вызываем родительский метод, 
        # чтобы работа CBV продолжилась.
        return super().dispatch(request, *args, **kwargs)
    
    # либо так - с PermissionDenied(выбор зависит от требований к проекту)
    # def dispatch(self, request, *args, **kwargs):
        # При получении объекта не указываем автора.
        # Результат сохраняем в переменную.
        instance = get_object_or_404(Birthday, pk=kwargs['pk'])
        # Сверяем автора объекта и пользователя из запроса.
        if instance.author != request.user:
            # Здесь может быть как вызов ошибки, так и редирект на нужную страницу.
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class BirthdayDeleteView(LoginRequiredMixin, DeleteView):
    model = Birthday
    success_url = reverse_lazy('birthday:list')

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Birthday, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday
        )
        # Записываем в переменную form пустой объект формы.
        context['form'] = CongratulationForm()
        # Запрашиваем все поздравления для выбранного дня рождения.
        context['congratulations'] = (
            # Дополнительно подгружаем авторов комментариев,
            # чтобы избежать множества запросов к БД.
            self.object.congratulations.select_related('author')
        )
        return context


# Будут обработаны POST-запросы только от залогиненных пользователей.
@login_required
def add_comment(request, pk):
    # Получаем объект дня рождения или выбрасываем 404 ошибку.
    birthday = get_object_or_404(Birthday, pk=pk)
    # Функция должна обрабатывать только POST-запросы.
    form = CongratulationForm(request.POST)
    if form.is_valid():
        # Создаём объект поздравления, но не сохраняем его в БД.
        congratulation = form.save(commit=False)
        # В поле author передаём объект автора поздравления.
        congratulation.author = request.user
        # В поле birthday передаём объект дня рождения.
        congratulation.birthday = birthday
        # Сохраняем объект в БД.
        congratulation.save()
    # Перенаправляем пользователя назад, на страницу дня рождения.
    return redirect('birthday:detail', pk=pk)
# ...
# Либо мы можем описать функцию add_comment выше иначе - с помощью CBV:
# class CongratulationCreateView(LoginRequiredMixin, CreateView):
    birthday = None
    model = Congratulation
    form_class = CongratulationForm

    # Переопределяем dispatch()
    def dispatch(self, request, *args, **kwargs):
        self.birthday = get_object_or_404(Birthday, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    # Переопределяем form_valid()
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.birthday = self.birthday
        return super().form_valid(form)

    # Переопределяем get_success_url()
    def get_success_url(self):
        return reverse('birthday:detail', kwargs={'pk': self.birthday.pk})
    # А чтобы вся эта красота заработала — надо поменять маршрут 
    # и вместо функции add_comment() указать CongratulationCreateView.as_view(), 
    # как и полагается при работе с CBV.
