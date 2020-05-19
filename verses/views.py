from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from verses.schema import VerseSchema, TagSchema, TranslationTagSchema, PurportSectionTagSchema
from common import api_exceptions
from common.helpers import get_filters
import json
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from verses.models import Verse, TranslationTag, PurportSectionTag, Tag3
from common.helpers import make_response, GET_SUCCESS_CODE, POST_SUCCESS_CODE, PUT_SUCCESS_CODE
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.utils import IntegrityError
from marshmallow import ValidationError as MarshmallowValidationError
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
        # TODO :- Need to handle validation of verse_id in POST and PUT updates
        req_data = json.loads(request.body)
        schema = (self.schema)()
        verse_details = req_data["verse_id"].split(".")
        req_data["canto_num"] = int(verse_details[0])
        req_data["chapter_num"] = int(verse_details[1])
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


class TagHandler(View):
    schema = TagSchema

    @api_exceptions.api_exception_handler
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(VerseHandler, self).dispatch(*args, **kwargs)

    def get(self, request):
        tags = self.schema.model.objects.all()
        schema = (self.schema)()
        data = schema.dump(tags)
        return JsonResponse(data)

class TagTranslationHandler(View):
    schema = TranslationTagSchema

    @api_exceptions.api_exception_handler
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(TagTranslationHandler, self).dispatch(*args, **kwargs)

    def get(self, request):
        verse_filter_params = {"verse__canto_num":"canto_num", "verse__chapter_num":"chapter_num"}
        tag_filter_params = {"verse__verse_id":"verse_id"}
        verse_filters = get_filters(request, verse_filter_params)
        tag_filters = get_filters(request, tag_filter_params)

        tag_objects = TranslationTag.objects.filter(**tag_filters).select_related("verse")
        tag_objects = tag_objects.filter(**verse_filters)
        print(tag_objects)
        schema = (self.schema)()
        data = schema.dump(tag_objects, many=True)
        resp_data = make_response(data, message="Successfully fetched verses", code=GET_SUCCESS_CODE)
        return JsonResponse(resp_data)

    @csrf_exempt
    def post(self, request):
        req_data = json.loads(request.body)
        schema = (self.schema)()
        try:
            new_translation_tag = schema.load(req_data)
        except MarshmallowValidationError as e:
            raise api_exceptions.BadRequestData(errors=e.messages)
        new_translation_tag["verse"] = Verse.objects.get(verse_id=new_translation_tag["verse_id"])
        new_translation_tag["tag"] = Tag3.objects.get(name=new_translation_tag["tag"])
        try:
            translation_tags = TranslationTag.objects.create(**new_translation_tag)
        except DjangoValidationError as e:
            raise api_exceptions.ValidationError(errors=e.message_dict)
        except IntegrityError as e:
            raise api_exceptions.ValidationError(errors="DB Integrity error")
        resp_data = schema.dump(translation_tags)
        resp_data = make_response(resp_data, message="Successfully added translation tag", code=PUT_SUCCESS_CODE)
        return JsonResponse(resp_data)

class TagPurportSectionHandler(View):
    schema = PurportSectionTagSchema

    @api_exceptions.api_exception_handler
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(TagPurportSectionHandler, self).dispatch(*args, **kwargs)

    def get(self, request):
        verse_filter_params = {"verse__canto_num":"canto_num", "verse__chapter_num":"chapter_num"}
        tag_filter_params = {"verse__verse_id":"verse_id"}
        verse_filters = get_filters(request, verse_filter_params)
        tag_filters = get_filters(request, tag_filter_params)

        tag_objects = TagPurportSectionHandler.objects.filter(**tag_filters).select_related("verse")
        tag_objects = tag_objects.filter(**verse_filters)
        print(tag_objects)
        schema = (self.schema)()
        data = schema.dump(tag_objects, many=True)
        resp_data = make_response(data, message="Successfully fetched translation tags", code=GET_SUCCESS_CODE)
        return JsonResponse(resp_data)

    @csrf_exempt
    def post(self, request):
        req_data = json.loads(request.body)
        schema = (self.schema)()
        try:
            new_purport_section_tag = schema.load(req_data)
        except MarshmallowValidationError as e:
            raise api_exceptions.BadRequestData(errors=e.messages)
        try:
            new_purport_section_tag["tag"] = Tag3.objects.get(name=new_purport_section_tag["tag"])
            purport_section_tags = PurportSectionTag.objects.create(**new_purport_section_tag)
        except DjangoValidationError as e:
            raise api_exceptions.ValidationError(errors=e.message_dict)
        except IntegrityError as e:
            raise api_exceptions.ValidationError(errors="DB Integrity error")
        resp_data = schema.dump(purport_section_tags)
        return JsonResponse(resp_data)