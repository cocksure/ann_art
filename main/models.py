import os
from io import BytesIO

from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


def process_image(image, upload_path, quality=70, max_size=(1024, 1024)):
    try:
        img = Image.open(image)

        # Проверка формата
        if img.format and img.format.lower() not in ['jpg', 'jpeg', 'png', 'webp']:
            raise ValueError(f"Неподдерживаемый формат: {img.format}")

        # Сжатие по размеру
        if img.width > max_size[0] or img.height > max_size[1]:
            img.thumbnail(max_size, Image.LANCZOS)

        # Подготовка к сохранению
        output = BytesIO()
        img.save(output, format='WEBP', quality=quality, optimize=True)
        output.seek(0)

        # Генерация безопасного имени
        filename_wo_ext = os.path.splitext(os.path.basename(image.name))[0]
        safe_name = slugify(filename_wo_ext) + '.webp'

        full_path = os.path.join(upload_path, safe_name)

        return full_path, ContentFile(output.read())

    except Exception as e:
        raise ValueError(f"Ошибка при обработке изображения: {e}")


class MaterialCategory(models.Model):
    name = models.CharField(
        _('Название категории'),
        max_length=100,
        unique=True
    )
    description = models.TextField(
        _('Описание'),
        null=True,
        blank=True
    )
    order = models.PositiveIntegerField(
        _('Порядок отображения'),
        default=0,
        null=True,
        blank=True
    )
    image = models.ImageField(
        _('Фото категории'),
        upload_to='category_images/',
        blank=True,
        default='default_foto.png',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'heic'])]
    )

    def save(self, *args, **kwargs):
        if self.image:
            new_name, new_file = process_image(self.image, "style_images/")

            if self.pk:
                try:
                    old_instance = self.__class__.objects.get(pk=self.pk)
                    if (
                            old_instance.image
                            and old_instance.image != self.image
                            and old_instance.image.name != settings.DEFAULT_IMAGE
                    ):
                        old_instance.image.delete(save=False)
                except self.__class__.DoesNotExist:
                    pass

            self.image.save(new_name, new_file, save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Категория материала')
        verbose_name_plural = _('Категории материалов')


class MaterialItem(models.Model):
    category = models.ForeignKey(
        MaterialCategory,
        on_delete=models.CASCADE,
        verbose_name=_('Категория'),
        default=None
    )
    title = models.CharField(
        _('Заголовок'),
        max_length=255,
        unique=True
    )
    description = models.TextField(
        _('Описание'),
        null=True,
        blank=True
    )
    image = models.ImageField(
        _('Изображение'),
        upload_to='materials/',
        null=True,
        blank=True
    )
    order = models.PositiveIntegerField(
        _('Порядок'),
        default=0,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if self.image:
            new_name, new_file = process_image(self.image, "style_images/")

            if self.pk:
                try:
                    old_instance = self.__class__.objects.get(pk=self.pk)
                    if (
                            old_instance.image
                            and old_instance.image != self.image
                            and old_instance.image.name != settings.DEFAULT_IMAGE
                    ):
                        old_instance.image.delete(save=False)
                except self.__class__.DoesNotExist:
                    pass

            self.image.save(new_name, new_file, save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.category.name})"

    class Meta:
        ordering = ('order',)
        verbose_name = _('Материал')
        verbose_name_plural = _('Материалы')


class StyleItem(models.Model):
    title = models.CharField(
        _('Название стиля'),
        max_length=255
    )
    description = models.TextField(
        _('Описание')
    )
    image = models.ImageField(
        _('Изображение'),
        upload_to='styles/'
    )
    order = models.PositiveIntegerField(
        _('Порядок'),
        default=0
    )

    def save(self, *args, **kwargs):
        if self.image:
            new_name, new_file = process_image(self.image, "style_images/")

            if self.pk:
                try:
                    old_instance = self.__class__.objects.get(pk=self.pk)
                    if (
                            old_instance.image
                            and old_instance.image != self.image
                            and old_instance.image.name != settings.DEFAULT_IMAGE
                    ):
                        old_instance.image.delete(save=False)
                except self.__class__.DoesNotExist:
                    pass

            self.image.save(new_name, new_file, save=False)

        super().save(*args, **kwargs)

    class Meta:
        ordering = ('order',)
        verbose_name = "Стиль"
        verbose_name_plural = "Стили"

    def __str__(self):
        return self.title


class ProjectItem(models.Model):
    class ProjectType(models.TextChoices):
        COMMERCIAL = 'commercial', _('Коммерческие помещения')
        RESIDENTIAL = 'residential', _('Жилые помещения')
        OTHER = 'other', _('Другое')

    title = models.CharField(
        _('Название проекта'),
        max_length=255
    )
    description = models.TextField(
        _('Описание'),
        blank=True,
        null=True
    )
    image = models.ImageField(
        _('Изображение'),
        upload_to='projects/'
    )
    order = models.PositiveIntegerField(
        _('Порядок'),
        default=0,
        null=True,
        blank=True
    )
    category = models.CharField(
        _('Тип проекта'),
        max_length=20,
        choices=ProjectType.choices,
        default=ProjectType.OTHER,
    )

    def save(self, *args, **kwargs):
        if self.image:
            new_name, new_file = process_image(self.image, "style_images/")

            if self.pk:
                try:
                    old_instance = self.__class__.objects.get(pk=self.pk)
                    if (
                            old_instance.image
                            and old_instance.image != self.image
                            and old_instance.image.name != settings.DEFAULT_IMAGE
                    ):
                        old_instance.image.delete(save=False)
                except self.__class__.DoesNotExist:
                    pass

            self.image.save(new_name, new_file, save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Проект')
        verbose_name_plural = _('Проекты')
        ordering = ['order']


class ServiceItem(models.Model):
    title = models.CharField(
        _('Название услуги'),
        max_length=255
    )
    description = models.TextField(
        _('Краткое описание')
    )
    details = models.TextField(
        _('Детали (HTML или Markdown)'),
        blank=True
    )
    order = models.PositiveIntegerField(
        _('Порядок'),
        default=0
    )

    class Meta:
        verbose_name = _('Услуга')
        verbose_name_plural = _('Услуги')
        ordering = ['order', 'id']

    def __str__(self):
        return f"[{self.order:02}] {self.title}"


class GuaranteeItem(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    description = models.TextField("Описание")
    order = models.PositiveIntegerField("Порядок", default=0)

    def __str__(self):
        return self.title


class InstallmentInfo(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    paragraph1 = models.TextField("Первый блок текста")
    paragraph2 = models.TextField("Второй блок текста")
    paragraph3 = models.TextField("Третий блок текста")
    button_text = models.CharField("Текст кнопки", max_length=100, default="Узнать условия")
    button_link = models.CharField("Ссылка", max_length=255, default="#contact")

    def __str__(self):
        return "Информация о рассрочке"


class Partners(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения", null=True, blank=True)
    image = models.ImageField(
        upload_to="partners/",
        blank=True,
        verbose_name="Фото партнеры",
        default='default_foto.png',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'heic'])]
    )

    def save(self, *args, **kwargs):
        if self.image:
            new_name, new_file = process_image(self.image, "style_images/")

            if self.pk:
                try:
                    old_instance = self.__class__.objects.get(pk=self.pk)
                    if (
                            old_instance.image
                            and old_instance.image != self.image
                            and old_instance.image.name != settings.DEFAULT_IMAGE
                    ):
                        old_instance.image.delete(save=False)
                except self.__class__.DoesNotExist:
                    pass

            self.image.save(new_name, new_file, save=False)

        super().save(*args, **kwargs)

    # def __str__(self):
    #     return self.name

    class Meta:
        ordering = ('order',)
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"
