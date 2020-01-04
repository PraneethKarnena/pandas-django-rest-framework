from django.db import models


class DatasetModel(models.Model):

    file = models.FileField(null=False, blank=False)
    size = models.TextField(null=True, blank=True)

    STATUS_CHOICES = (
        ('PEN', 'Pending'),
        ('CRT', 'Created'),
    )

    dataframe_file_name = models.TextField(null=True, blank=True)
    dataframe_creation_status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='PEN')
    dataframe_url = models.URLField(null=True, blank=True)

    excel_file_name = models.TextField(null=True, blank=True)
    excel_creation_status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='PEN')
    excel_url = models.URLField(null=True, blank=True)

    stats = models.TextField(null=True, blank=True)
    stats_creation_status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='PEN')

    pdf_file_name = models.TextField(null=True, blank=True)
    pdf_creation_status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='PEN')
    pdf_url = models.URLField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.file.name} - {self.created_at}'