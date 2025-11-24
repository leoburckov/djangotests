from django.db import models
from django.conf import settings


class Product(models.Model):
    PUBLISH_STATUS = [
        ('published', 'Опубликован'),
        ('moderation', 'На модерации'),
        ('rejected', 'Отклонен'),
    ]

    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Изображение')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    # Сначала сделаем поле nullable
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        related_name='products',
        null=True,  # Временно разрешаем null
        blank=True  # Временно разрешаем blank
    )
    status = models.CharField(
        max_length=20,
        choices=PUBLISH_STATUS,
        default='moderation',
        verbose_name='Статус публикации'
    )
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
            ("can_change_status", "Может изменять статус продукта"),
        ]

    def __str__(self):
        return self.name

    def can_edit(self, user):
        """Может ли пользователь редактировать продукт"""
        if not self.owner:  # Если владелец не установлен
            return user.is_superuser
        return user == self.owner

    def can_delete(self, user):
        """Может ли пользователь удалить продукт"""
        if not self.owner:  # Если владелец не установлен
            return user.is_superuser or user.has_perm('catalog.delete_product')
        return user == self.owner or user.has_perm('catalog.delete_product')

    def can_change_status(self, user):
        """Может ли пользователь изменять статус продукта"""
        return user.has_perm('catalog.can_change_status') or user.has_perm('catalog.can_unpublish_product')


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name