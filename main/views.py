
from json import loads, JSONDecodeError

from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView


class ListView(TemplateView):

    template_name = 'main/list.html'

    def get_context_data(self):
        """The Web 2.0/REST way would be to load a page with an empty table
        and then have the JavaScript perform a request to get a list of
        Contacts"""

        return {
            # replace this list of dicts with a queryset of
            'contacts': [
                {
                    'pk': 1000000,
                    'first_name': 'aaron',
                    'last_name': 'aaronson',
                    'mobile_phone': '614-555-0001',
                    'email': 'aaaa@example.com'
                },
                {
                    'pk': 1000001,
                    'first_name': 'betty',
                    'last_name': 'bailey',
                    'mobile_phone': '614-555-0001',
                    'email': 'betty.bailey@example.com',
                },
            ]
        }


class ContactRestView(View):
    """Django REST framework is better for this sort of thing."""

    ERROR_INVALID_JSON = 1
    ERROR_PK_ALREADY_SET = 2

    FIELDS_AND_LABELS = {
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'mobile_phone': 'Mobile Phone',
        'email': 'Email',
    }

    @staticmethod
    def generic_error_message(error_code):
        return f"Invalid request.  Error code {error_code}"

    @staticmethod
    def error_response(errors):
        """
        param errors:  A list of strings
        """
        return JsonResponse(
            {'errors': errors},
            status=400,
        )


class ContactNewRestView(ContactRestView):

    def post(self, request, *args, **kwargs):
        try:
            contact_json = loads(request.body)
        except JSONDecodeError:
            return self.error_response(
                [self.generic_error_message(self.ERROR_INVALID_JSON)],
            )

        if contact_json.get('pk'):
            return self.error_response(
                [self.generic_error_message(self.ERROR_PK_ALREADY_SET)],
            )

        errors = []
        for field, label in self.FIELDS_AND_LABELS.items():
            value = contact_json.get(field)
            if value:
                if not isinstance(value, str):
                    errors.append(f"{value!r} is not a string")
            else:
                errors.append(f"Missing {label}")





        return JsonResponse(contact_json, status=201)


class ContactUpdateRestView(ContactRestView):
    """Django REST framework is better for this sort of thing."""

    def put(self, request, *args, **kwargs):
        """Update a Contact"""
        return JsonResponse({}, status=200)
