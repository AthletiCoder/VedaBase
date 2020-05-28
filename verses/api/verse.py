from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from verses.schema import VerseSchema
from common import api_exceptions
from common.helpers import get_filters, api_token_required
import json
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from verses.models import Verse, TranslationTag, PurportSectionTag, Tag3
from common.helpers import make_response, GET_SUCCESS_CODE, POST_SUCCESS_CODE, PUT_SUCCESS_CODE
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.utils import IntegrityError
from marshmallow import ValidationError as MarshmallowValidationError

class VerseHandler(View):
    schema = VerseSchema

    @method_decorator(api_exceptions.api_exception_handler)
    @method_decorator(api_token_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(VerseHandler, self).dispatch(*args, **kwargs)

    def get(self, request):
        filter_params = {}
        filters = ["verse_id", "canto_num", "chapter_num", "verse_num"]
        for key in filters:
            if request.GET.get(key):
                filter_params[key] = request.GET.get(key)
        verses = Verse.objects.filter(**filter_params)
        schema = (self.schema)()
        data = schema.dump(verses, many=True)
        resp_data = make_response(data, message="Successfully fetched verses", code=GET_SUCCESS_CODE)
        return JsonResponse(resp_data)

    @csrf_exempt
    def post(self, request):
        # TODO :- Need to handle validation of verse_id in POST and PUT updates
        req_data = json.loads(request.body)
        schema = (self.schema)()
        verse_details = req_data["verse_id"].split(".")
        req_data["canto_num"] = int(verse_details[0])
        req_data["chapter_num"] = int(verse_details[1])
        if '-' in verse_details[2]:
            start, end = verse_details[2].split("-")
            req_data["verse_num"] = int(start)
            req_data["verse_num_end"] = int(end)
        else:
            req_data["verse_num"] = int(verse_details[2])
        try:
            new_verses_data = schema.load(req_data)
        except MarshmallowValidationError as e:
            raise api_exceptions.BadRequestData(errors=e.messages)
        try:
            new_verses = Verse.objects.create(**new_verses_data)
        except DjangoValidationError as e:
            raise api_exceptions.ValidationError(errors=e.message_dict)
        except IntegrityError as e:
            raise api_exceptions.ValidationError(errors="DB Integrity error")
        resp_data = schema.dump(new_verses)
        return JsonResponse(resp_data)

    @csrf_exempt
    def put(self, request):
        req_data = json.loads(request.body)
        schema = (self.schema)()
        try:
            verse_updates = schema.load(req_data, partial=('verse','translation', 'purport')) 
        except MarshmallowValidationError as e:
            raise api_exceptions.BadRequestData(errors=e.messages)
        remove = ['chapter_num','canto_num','verse_num']
        for item in remove:
            if item in verse_updates.keys():
                del verse_updates[item]
        verse_obj = Verse.objects.filter(verse_id=req_data["verse_id"])
        if not verse_obj:
            raise api_exceptions.ValidationError(errors="Verse doesn't exist")
        try:
            verse_obj.update(**verse_updates)
        except (DjangoValidationError, IntegrityError) as e:
            raise api_exceptions.ValidationError(errors=e.message_dict)

        resp_data = make_response({}, message="Successfully updated verse", code=PUT_SUCCESS_CODE)
        return JsonResponse(resp_data)