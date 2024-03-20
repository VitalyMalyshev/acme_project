from django.shortcuts import render, get_object_or_404, redirect
from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown


# Импортируйте в файл birthday/views.py класс ListView и CreateView,
from django.views.generic import ListView, CreateView, UpdateView
# Путь для редиректа указывается в функции reverse_lazy(): 
# она, как и функция reverse(), возвращает строку с URL нужной страницы.
# Однако reverse_lazy() срабатывает только при непосредственном обращении к CBV
# во время работы веб-сервера, а не на этапе запуска проекта, когда импортируются все классы. 
# В момент запуска проекта карта маршрутов может быть ещё не сформирована, 
# и использование обычного reverse() вызовет ошибку.
from django.urls import reverse_lazy


# Новый класс вместо функции birthday(ее пока оставим в коде)
class BirthdayCreateView(CreateView):
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # Указываем имя формы(Класс CreateView может создать собственную форму, но может использовать форму,
    # созданную отдельно, через класс ModelForm. ):
    form_class = BirthdayForm
    # Этот класс сам может создать форму на основе модели!
    # Нет необходимости отдельно создавать форму через ModelForm.
    # Указываем поля, которые должны быть в форме:
    # fields = '__all__'
    # Как и в классе ListView, в описании класса CreateView необязательно указывать имя шаблона, 
    # но тогда шаблон должен называться по схеме имя-модели_form.html, то есть в нашем проекте 
    # имя шаблона должно быть birthday_form.html. В приложении birthday шаблон называется иначе, 
    # так что его название нужно указать в явном виде через атрибут template_name.
    # Явным образом указываем шаблон(или переименовываем его в birthday_form.html):
    template_name = 'birthday/birthday.html' 
    # Указываем namespace:name страницы, куда будет перенаправлен пользователь
    # после создания объекта:
    success_url = reverse_lazy('birthday:list')


# Пока оставим в коде, но уже есть новый класс выше и функция не нужна
def birthday(request, pk=None):
    if pk is not None:
        instance = get_object_or_404(Birthday, pk=pk)
    else:
        instance = None
    form = BirthdayForm(
        request.POST or None,
        files=request.FILES or None,
        instance=instance
    )
    context = {'form': form}
    if form.is_valid():
        form.save()
        birthday_countdown = calculate_birthday_countdown(
            form.cleaned_data['birthday']
        )
        context.update({'birthday_countdown': birthday_countdown})
    return render(request, 'birthday/birthday.html', context)


# Наследуем класс от встроенного ListView:
class BirthdayListView(ListView):
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # ...сортировку, которая будет применена при выводе списка объектов:
    ordering = 'id'
    # ...и даже настройки пагинации:
    paginate_by = 10

# Класс UpdateView — редактирование объекта(edit)
class BirthdayUpdateView(UpdateView):
    model = Birthday
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'
    success_url = reverse_lazy('birthday:list')


def delete_birthday(request, pk):
    instance = get_object_or_404(Birthday, pk=pk)
    form = BirthdayForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('birthday:list')
    return render(request, 'birthday/birthday.html', context)
