from django.db import models
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    """Show only published posts"""
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=200, verbose_name="Название поста")
    slug = models.SlugField(
        max_length=200,
        unique_for_date='publish',
        verbose_name='Текст "slug"'

    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        verbose_name="Автор",

    )
    body = models.TextField(verbose_name="Текст поста")
    publish = models.DateTimeField(default=timezone.now, verbose_name="Дата публикации")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="Статус"
    )
    tags = models.ManyToManyField('Tag',
                                 help_text="Выберите тег",
                                 verbose_name="Теги",
                                 null=True, blank=True,
                                 )

    objects = models.Manager
    # published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return f'{self.title[:15]}...'

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[
                           self.publish.year,
                           self.publish.month,
                           self.publish.day,
                           self.slug]
                       )


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by { self.name } on { self.post }'


class Tag(models.Model):
    tag_name = models.CharField(max_length=10,
                                unique=True,
                                help_text="format - #*** some word.",
                                verbose_name="Теги",

                                )

    objects = models.Manager

    class Meta:
        ordering = ('tag_name',)

    def __str__(self):
        return f'{self.tag_name}'
