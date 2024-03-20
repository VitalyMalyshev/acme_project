from django.urls import path

from . import views

app_name = 'birthday'

urlpatterns = [
    # Перенастроим путь для нового класса BirthdayCreateView(вместо функции birthday()):
    path('', views.BirthdayCreateView.as_view(), name='create'),
    # Теперь перенастроим маршрутизацию: в файле birthday/urls.py в маршруте с name='list' 
    # замените вызов view-функции birthday_list на обращение к методу as_view() класса BirthdayListView. 
    # Этот метод есть у всех встроенных CBV и наследуется в пользовательских классах.
    path('list/', views.BirthdayListView.as_view(), name='list'),
    # и тут подправили:
    path('<int:pk>/edit/', views.BirthdayUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.BirthdayDeleteView.as_view(), name='delete'),
]
