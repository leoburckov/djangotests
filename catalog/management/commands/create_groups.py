from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группы модераторов и назначает права'

    def handle(self, *args, **options):
        # Создаем группу модераторов
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        # Получаем разрешения
        content_type = ContentType.objects.get_for_model(Product)

        # Право на отмену публикации
        unpublish_permission, _ = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            name='Может отменять публикацию продукта',
            content_type=content_type,
        )

        # Право на изменение статуса
        change_status_permission, _ = Permission.objects.get_or_create(
            codename='can_change_status',
            name='Может изменять статус продукта',
            content_type=content_type,
        )

        # Право на удаление любого продукта
        delete_permission = Permission.objects.get(
            codename='delete_product',
            content_type=content_type,
        )

        # Назначаем права группе
        moderator_group.permissions.add(
            unpublish_permission,
            change_status_permission,
            delete_permission
        )

        self.stdout.write(
            self.style.SUCCESS('Группа "Модератор продуктов" создана с правами:')
        )
        self.stdout.write(
            self.style.SUCCESS('- Отмена публикации продукта')
        )
        self.stdout.write(
            self.style.SUCCESS('- Изменение статуса продукта')
        )
        self.stdout.write(
            self.style.SUCCESS('- Удаление любого продукта')
        )