from django.db import models


class MaterialItem(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="materials/")
    order = models.PositiveIntegerField("Порядок", default=0)

    def __str__(self):
        return self.title


class StyleItem(models.Model):
    title = models.CharField("Название стиля", max_length=255)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="styles/")
    order = models.PositiveIntegerField("Порядок", default=0)

    def __str__(self):
        return self.title


class ProjectItem(models.Model):
    title = models.CharField("Название проекта", max_length=255)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Изображение", upload_to="projects/")
    order = models.PositiveIntegerField("Порядок", default=0)

    def __str__(self):
        return self.title


class ServiceItem(models.Model):
    title = models.CharField("Название услуги", max_length=255)
    description = models.TextField("Краткое описание")
    details = models.TextField("Детали (HTML или Markdown)", blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)

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
