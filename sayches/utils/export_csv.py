import csv

from django.http import HttpResponse


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


def export_ads_history(request, ads):
    ad_status = {
        '1': 'Approved',
        '2': 'Rejected',
        '3': 'Pending',
        '4': 'Suspended',
    }
    ads_history_data = ads.values_list('slug', 'ad_headline', 'ad_link', 'ad_body', 'ad_image', 'ad_location',
                                       'ad_start_date', 'ad_end_date', 'ad_plan__title', 'status', 'amount_due',
                                       'clicks')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=ads_history.csv'
    writer = csv.writer(response)
    writer.writerow(
        ['#', 'Headline', 'Link', 'Body', 'Image', 'Location', 'Start Date', 'End Date', 'Plan', 'Status', 'Cost',
         'Clicks'])
    for ads in ads_history_data:
        ads = list(ads)
        ads[9] = ad_status.get(ads[9])
        writer.writerow(ads)
    return response
