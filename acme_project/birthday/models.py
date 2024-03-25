from django.db import models
from .validators import real_age
# Импортируем функцию reverse() для получения ссылки на объект.
from django.urls import reverse
# Импортируем модуль для обращения к объекту пользователя,
# чтобы потом связать его c моделю Birthday:
from django.contrib.auth import get_user_model


# Именно так всегда и ссылаемся на модель пользователя:
User = get_user_model()

class Birthday(models.Model):
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField(
        'Фамилия', blank=True, help_text='Необязательное поле', max_length=20
    )
    # Валидатор указывается в описании поля.
    birthday = models.DateField('Дата рождения', validators=(real_age,))
    # Поле с картинкой
    image = models.ImageField('Фото', upload_to='birthdays_images', blank=True)
    # Код для связи юзера(автора поста с моделью):
    author = models.ForeignKey(
        User, verbose_name='Автор записи', on_delete=models.CASCADE, null=True
    )

    class Meta():
        constraints = (
            models.UniqueConstraint(
                fields=('first_name', 'last_name', 'birthday'),
                name='Unique person constraint',
            ),
        )

    def get_absolute_url(self):
        # С помощью функции reverse() возвращаем URL объекта.
        return reverse('birthday:detail', kwargs={'pk': self.pk})



