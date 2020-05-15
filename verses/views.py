from django.shortcuts import render
from django.views.generic import View
from verses.models import Verse
from django.http import JsonResponse
from verses.schema import VerseSchema, TagSchema
from common import api_exceptions
import json
# Create your views here.

class VerseHandler(View):
    schema = VerseSchema

    def get(self, request):
        verses = Verse.objects.all()
        schema = (self.schema)()
        data = schema.dump(verses)
        return JsonResponse(data)

    def post(self, request):
        req_data = json.loads(request.body)
        schema = (self.schema)()
        new_verses, errors = schema.load(req_data)
        if errors:
            raise api_exceptions.BadRequestData(errors)
        new_verses = self.schema.model.create()
        resp_data = schema.dump(new_verses)
        return JsonResponse(resp_data)

class TagHandler(View):
    schema = TagSchema

    def get(self, request):
        tags = Tag1.objects.all()
        schema = (self.schema)()
        data = schema.dump(tags)
        return JsonResponse(data)