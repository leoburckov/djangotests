import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product, Category


class Command(BaseCommand):
    help = 'Загрузка тестовых данных продуктов и категорий из фикстур'

    def add_arguments(self, parser):
        # Добавляем опциональный аргумент для подтверждения удаления
        parser.add_argument(
            '--force',
            action='store_true',
            help='Пропустить подтверждение удаления данных',
        )

    def handle(self, *args, **options):
        force = options['force']

        # Проверяем, есть ли данные для удаления
        product_count = Product.objects.count()
        category_count = Category.objects.count()

        self.stdout.write(
            self.style.WARNING(f'Найдено продуктов: {product_count}')
        )
        self.stdout.write(
            self.style.WARNING(f'Найдено категорий: {category_count}')
        )

        # Запрос подтверждения, если не указан флаг --force
        if not force:
            confirm = input(
                'Вы уверены, что хотите удалить все данные и загрузить новые? (y/N): '
            )
            if confirm.lower() != 'y':
                self.stdout.write(self.style.WARNING('Операция отменена'))
                return

        # Удаляем все существующие данные
        self.stdout.write('Удаление существующих данных...')

        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS('✅ Существующие данные удалены')
        )

        # Загружаем данные из фикстур
        fixture_dir = 'catalog/fixtures'

        try:
            # Загружаем категории первыми, так как продукты ссылаются на них
            self.stdout.write('Загрузка категорий...')
            call_command('loaddata', 'category_data.json')
            self.stdout.write(
                self.style.SUCCESS('✅ Категории успешно загружены')
            )

            # Загружаем продукты
            self.stdout.write('Загрузка продуктов...')
            call_command('loaddata', 'product_data.json')
            self.stdout.write(
                self.style.SUCCESS('✅ Продукты успешно загружены')
            )

            # Выводим итоговую статистику
            new_product_count = Product.objects.count()
            new_category_count = Category.objects.count()

            self.stdout.write(
                self.style.SUCCESS(
                    f'🎉 Загрузка завершена! '
                    f'Загружено {new_category_count} категорий и {new_product_count} продуктов'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Ошибка при загрузке данных: {e}')
            )