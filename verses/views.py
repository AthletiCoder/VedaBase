from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from verses.schema import VerseSchema, TagSchema
from common import api_exceptions
import json
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from verses.models import Verse
from common.helpers import make_response, GET_SUCCESS_CODE, POST_SUCCESS_CODE, PUT_SUCCESS_CODE
from django.core.exceptions import ValidationError as DjangoValidationError
# Create your views here.

class VerseHandler(View):
    schema = VerseSchema

    @api_exceptions.api_exception_handler
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
        req_data = json.loads(request.body)
        schema = (self.schema)()
        verse_details = req_data["verse_id"].split(".")
        req_data["canto_num"] = int(verse_details[0])
        req_data["chapter_num"] = int(verse_details[1])
        req_data["verse_num"] = int(verse_details[2])
        new_verses_data = schema.load(req_data)
        print(new_verses_data)
        try:
            new_verses = Verse.objects.create(**new_verses_data)
        except DjangoValidationError as e:
            raise api_exceptions.ValidationError(errors=e.message_dict)
        resp_data = schema.dump(new_verses)
        return JsonResponse(resp_data)

    @csrf_exempt
    def put(self, request):
        req_data = json.loads(request.body)
        schema = (self.schema)()
        verse_updates = schema.load(req_data, partial=('verse','translation', 'purport'))
        remove = ['chapter_num','canto_num','verse_num']
        for item in remove:
            if item in verse_updates.keys():
                del verse_updates[item]
        verse_obj = Verse.objects.filter(verse_id=req_data["verse_id"])
        if not verse_obj:
            raise api_exceptions.ValidationError(errors="Verse doesn't exist")
        try:
            verse_obj.update(**verse_updates)
        except DjangoValidationError as e:
            raise api_exceptions.ValidationError(errors=e.message_dict)

        resp_data = make_response({}, message="Successfully updated verse", code=PUT_SUCCESS_CODE)
        return JsonResponse(resp_data)

class TagHandler(View):
    schema = TagSchema

    def get(self, request):
        tags = self.schema.model.objects.all()
        schema = (self.schema)()
        data = schema.dump(tags)
        return JsonResponse(data)