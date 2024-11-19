"""
Модуль миксинов для панели администратора
ExportAsCSVMixin: предназначен для экспорта данных опроса в CSV формат
"""

import csv

from django.db.models import QuerySet
from django.db.models.options import Options
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet
from django.db.models.options import Options
from django.http import HttpRequest, HttpResponse


class ExportAsCSVMixin:
    def export_csv(self, request: HttpRequest, queryset: QuerySet):
        """
        Экспортирует данные в CSV
        """
        meta: Options = self.model._meta

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta.model_name}-export.csv'
        csv_writer = csv.writer(response)

        for survey in queryset:
            for question in survey.questions.all():
                csv_writer.writerow([question.nameTitleQuestion + ':'])
                for answer in question.answers.all():
                    answer_text = f'    {answer.text}: {answer.count}'
                    csv_writer.writerow([answer_text])
                    for choice in answer.choices.all():
                        choice_text = f'       {choice.text}: {choice.count}'
                        csv_writer.writerow([choice_text])

        return response

    export_csv.short_description = 'Export as CSV'


# import csv

# from django.db.models import QuerySet
# from django.db.models.options import Options
# from django.http import HttpRequest, HttpResponse


# class ExportAsCSVMixin:
#     def export_csv(self, request: HttpRequest, queryset: QuerySet):
#         """
#         Экспортирует данные в CSV
#         """
#         meta: Options = self.model._meta
#         field_names = [field.name for field in meta.fields]

#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = f'attachment; filename={meta}-export.csv'
#         csv_writer = csv.writer(response)

#         csv_writer.writerow(field_names)
#         for obj in queryset:
#             row = [str(getattr(obj, field)) for field in field_names]
#             csv_writer.writerow(row)

#         return response

#     export_csv.short_description = 'Export as CSV'
