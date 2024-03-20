from django.shortcuts import render, get_object_or_404, redirect
from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


# Создаём миксин.
class BirthdayMixin:
    model = Birthday
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'
    success_url = reverse_lazy('birthday:list')


# Добавляем миксин первым по списку родительских классов.
class BirthdayCreateView(BirthdayMixin, CreateView):
    # Не нужно описывать атрибуты: все они унаследованы от BirthdayMixin.
    pass


class BirthdayUpdateView(BirthdayMixin, UpdateView):
    # И здесь все атрибуты наследуются от BirthdayMixin.
    pass



# Наследуем класс от встроенного ListView - список объектов:
class BirthdayListView(ListView):
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # ...сортировку, которая будет применена при выводе списка объектов:
    ordering = 'id'
    # ...и даже настройки пагинации:
    paginate_by = 10

class BirthdayDeleteView(DeleteView):
    # Теперь, когда есть шаблон с тем именем, которое ожидает класс DeleteView:
    # birthday_confirm_delete.html, 
    # то из описания класса можно удалить вызов шаблона: 
    # template_name = 'birthday/birthday.html' и останется только 2 строки:
    model = Birthday
    success_url = reverse_lazy('birthday:list') 


def delete_birthday(request, pk):
    instance = get_object_or_404(Birthday, pk=pk)
    form = BirthdayForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('birthday:list')
    return render(request, 'birthday/birthday.html', context)
