from django.urls import path

from . import views

app_name = 'birthday'

urlpatterns = [
    path('', views.BirthdayCreateView.as_view(), name='create'),
    path('list/', views.BirthdayListView.as_view(), name='list'),
    # В Django есть специальный view-класс для отображения отдельных объектов:
    # DetailView. Унаследуем от него собственный класс — BirthdayDetailView;
    # отображать отдельные записи будем на страницах с адресом вида birthday/<pk>/:
    path('<int:pk>/', views.BirthdayDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.BirthdayUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.BirthdayDeleteView.as_view(), name='delete'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
]
