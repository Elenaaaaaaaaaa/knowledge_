import os
from django.utils.timezone import now
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField

# Create your models here.


class Tags(models.Model):
    tg_name = models.CharField('тэг', max_length=200, null=True, unique=True)

    def __str__(self):
        return self.tg_name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Calendar(models.Model):
    cal_date = models.DateField('Дата')
    cal_text = models.TextField('Текст')
    cal_tag = models.ManyToManyField(Tags, blank=True, verbose_name='Тэг')

    def __str__(self):
        return self.cal_text

    class Meta:
        verbose_name = 'Календарь'
        verbose_name_plural = 'Календарь'


class Problems(models.Model):
    STAT_dif = (('1', 'простая'), ('2', 'обычная'), ('3', 'сложная'), ('4', 'ОЧЕНЬ СЛОЖНАЯ'))
    STAT = (('актуально', 'актуально'), ('решено', 'решено'))
    pr_name = models.CharField('Наименование проблемы', max_length=100)
    pr_status = models.CharField('Статус', choices=STAT, max_length=50)
    pr_dif = models.CharField('Сложность', choices=STAT_dif, max_length=50)
    pr_solution = models.TextField('Решение')
    pr_document = models.FileField('Файл', blank=True)
    pr_calendar = models.ManyToManyField(Calendar, blank=True, verbose_name='События')

    def __str__(self):
        return self.pr_name

    class Meta:
        verbose_name = 'Проблема'
        verbose_name_plural = 'Проблемы'


class Tasks(models.Model):
    STAT_dif = (('1', 'простая'), ('2', 'обычная'), ('3', 'сложная'), ('4', 'ОЧЕНЬ СЛОЖНАЯ'))
    STAT = (('актуально', 'актуально'), ('выполнено', 'выполнено'))
    tk_name = models.CharField('Наименование задачи', max_length=50)
    tk_status = models.CharField('Статус', choices=STAT, max_length=50)
    tk_dif = models.CharField('Сложность', choices=STAT_dif, max_length=50)
    tk_type = models.ManyToManyField(Tags, blank=True, verbose_name='Тэг')
    tk_problem = models.ManyToManyField(Problems, blank=True, verbose_name='Проблемы')
    tk_calendar = models.ManyToManyField(Calendar,  blank=True, verbose_name='События')

    def __str__(self):
        return self.tk_name

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Projects(models.Model):
    STAT = (('открыт', 'открыт'), ('завершен', 'завершен'))
    pr_name = models.CharField('Название проекта', max_length=50)
    pr_team = models.ManyToManyField(User)
    pr_start = models.DateField('Начало работ')
    pr_deadline = models.DateField('Завершение работ')
    pr_status = models.CharField('Статус', choices=STAT, max_length=50)
    pr_calendar = models.ManyToManyField(Calendar, blank=True, verbose_name='События')
    pr_task = models.ManyToManyField(Tasks, blank=True, verbose_name='Задачи')

    def __str__(self):
        return self.pr_name

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class Messages(models.Model):
    mes_from = models.ForeignKey(User, related_name='author', on_delete=models.SET_NULL, null=True, verbose_name='От')
    mes_to = models.ManyToManyField(User, related_name='to',  verbose_name='Кому')
    mes_text = models.TextField('Текст сообщения')
    mes_tag = models.ManyToManyField(Tags)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Jobs(models.Model):
    job_name = models.CharField('должность', max_length=200, null=True, unique=True)

    def __str__(self):
        return self.job_name

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class Information(models.Model):
    info_employee = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Сотрудник')
    info_job = models.ManyToManyField(Jobs, blank=True, verbose_name='Должность')
    info_tel = PhoneField('Номер телефона', blank=True, help_text='Телефон | ext. ')
    info_image = models.ImageField('Фото', default="unnamed.png", null=True, blank=True)

    def __str__(self):
        return self.info_employee.get_username()

    def filename(self):
        return os.path.basename(self.info_image.name)

    class Meta:
        verbose_name = 'Информация о работнике'
        verbose_name_plural = 'Информация о работниках'


class Documents(models.Model):
    STAT = (('принят', 'принят'), ('на рассмотрении', 'на рассмотрении'), ('отклонен', 'отклонен'))
    doc_name = models.CharField('Название', max_length=50)
    doc_owner = models.ManyToManyField(User, 'Владельцы')
    doc_date = models.DateField('Последние изменения', default=datetime.now)
    doc_tag = models.ManyToManyField(Tags, 'Тэг')
    doc_doc = models.FileField('Файл', blank=True)
    doc_link = models.URLField('Ссылка на документ', blank=True, max_length=100)
    doc_calendar = models.ManyToManyField(Calendar, blank=True, verbose_name='События')
    doc_task = models.ForeignKey(Tasks, verbose_name='Задача', blank=True, null=True, on_delete=models.SET_NULL)
    doc_project = models.ManyToManyField(Projects, verbose_name='Для проекта')
    doc_acc = models.CharField('Статус', choices=STAT, null=True, max_length=50, default='на рассмотрении')

    def __str__(self):
        return self.doc_name

    def filename(self):
        return os.path.basename(self.doc_doc.name)

    class Meta:
        verbose_name = 'Документы'
        verbose_name_plural = 'Документы'


class Comments(models.Model):
    com_title = models.CharField('Заголовок комментария', max_length=50)
    com_user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.SET_NULL, null=True)
    com_text = models.TextField('Текст комментария')
    com_date = models.DateTimeField(default=now, editable=False)
    com_teg = models.ManyToManyField(Tags, blank=True, verbose_name='Тэг')
    com_doc = models.ManyToManyField(Documents, blank=True, verbose_name='Документы')
    com_proj = models.ForeignKey(Projects, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Проекты')
    com_tasks = models.ManyToManyField(Tasks, blank=True, verbose_name='Задачи')
    com_prob = models.ManyToManyField(Problems, blank=True, verbose_name='Проблемы')

    def __str__(self):
        return self.com_title

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'















