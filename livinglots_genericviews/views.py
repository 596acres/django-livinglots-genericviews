import csv

from django.contrib.contenttypes.models import ContentType
from django.core.serializers import json
from django.http import Http404, HttpResponse
from django.views.generic import View
from django.views.generic.edit import FormMixin


class CSVView(View):
    response_class = HttpResponse

    def get(self, request, *args, **kwargs):
        return self.render_to_response()

    def get_fields(self):
        """Get the fields (column names) for this CSV"""
        raise NotImplementedError

    def get_filename(self):
        """Get the filename for this CSV"""
        return 'download'

    def get_rows(self):
        """
        Get the rows for this CSV

        The rows must be dicts of field (column) names to field values.

        """
        raise NotImplementedError

    def write_csv(self, response):
        fields = self.get_fields()
        csv_file = csv.DictWriter(response, fields)

        # Write header
        response.write(','.join(['%s' % field.replace('_', ' ') for field in fields]))
        response.write('\n')

        # Write rows
        for row in self.get_rows():
            csv_file.writerow(row)

    def render_to_response(self):
        """
        Simple render to CSV.
        """
        response = self.response_class(mimetype='text/csv')
        response['Content-Disposition'] = ('attachment; filename="%s.csv"' %
                                           self.get_filename())
        self.write_csv(response)
        return response


class JSONResponseView(View):
    response_class = HttpResponse

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs):
        """Simple render to JSON"""
        return self.response_class(
            json.json.dumps(self.get_context_data(**self.kwargs),
                            cls=json.DjangoJSONEncoder, ensure_ascii=False),
            mimetype='application/json',
        )


class AddGenericMixin(FormMixin):
    """
    A mixin that eases adding content that references a model instance using a
    generic relationship. It adds the content_type and object_id for the
    relationship to the view's form's initial data.
    """
    content_type_model = None
    content_type_id_key = 'content_type_id'
    object_id_key = 'pk'

    def get_object_id_key(self):
        return self.object_id_key

    def get_content_type_id_key(self):
        return self.content_type_id_key

    def get_content_object(self):
        return self.get_content_type().get_object_for_this_type(
            pk=self.get_content_object_id()
        )

    def get_content_object_id(self):
        return self.kwargs[self.get_object_id_key()]

    def get_content_type(self):
        if self.content_type_model:
            return ContentType.objects.get_for_model(self.content_type_model)
        content_type_id = self.kwargs[self.get_content_type_id_key()]
        return ContentType.objects.get_for_id(content_type_id)

    def get_initial(self):
        """Add initial content_type and object_id to the form"""
        initial = super(AddGenericMixin, self).get_initial()
        try:
            content_type = self.get_content_type()
            object_id = self.kwargs[self.get_object_id_key()]
        except KeyError:
            raise Http404
        initial.update({
            'content_type': content_type,
            'object_id': object_id,
        })
        return initial
