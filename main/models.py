from importlib.resources import contents
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser
from .utilities import get_timestamp_path

class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошёл активацию?')
    send_messages = models.BooleanField(default=True, verbose_name='Высылать сообщения о новых комментариях?')

    def delete(self, *args, **kwargs):
        for board in self.board_set.all():
            board.delete()
        super().delete(*args, **kwargs)
    # удаление всех объявлений пользователя при удалении профиля

    class Meta(AbstractUser.Meta):
        pass

class Rubric(models.Model):
    name = models.CharField(max_length=30, 
        db_index=True, 
        unique=True, 
        verbose_name='Название')
    order = models.SmallIntegerField(default=0,
        db_index=True,
        verbose_name='Порядок')
    super_rubric = models.ForeignKey('SuperRubric',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Надрубрика')
    # базовая модель рубрик

class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)
        # условие фильтрации записей

class SuperRubric(Rubric):
    objects = SuperRubricManager()
    def __str__(self):
        return self.name
    # метод __str__ генерирует строковое представление рубрики (нзвание)

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Надрубрика'
        verbose_name_plural ='Надрубрики'

class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)

class SubRubric(Rubric):
    objects = SubRubricManager()
    def __str__(self):
        return '%s-%s' % (self.super_rubric.name, self.name)

    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order','name')
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'

class Board(models.Model):
    rubric = models.ForeignKey(SubRubric, on_delete=models.PROTECT, verbose_name='Рубрика')
    title = models.CharField(max_length=60, verbose_name='Товар либо услуга')
    content = models.TextField(verbose_name='Описание')
    price = models.FloatField(default=0, verbose_name='Цена')
    contacts = models.TextField(verbose_name='Контакты')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Изображение')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name='Автор объявления')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Выводить в списке?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    # функция get_timestamp_path даёт изображению имя временной отметки в момент его добавления 
    # (для приведению имён изображений к одному формату)

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs) 
        # удаление иллюстраций связанных с публикацией

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at'] # сортировка по последней дате
# модель публикации объявления
        
class AdditionalImage(models.Moodel):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, verbose_name='Объявление')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Дополнительная иллюстрация'
        verbose_name_plural = 'Дополнительные иллюстрации'










