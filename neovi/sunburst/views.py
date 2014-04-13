from django.shortcuts import render
from django.http import HttpResponse
from sunburst.Backend_parsing import Parser
import json

def index(request):
    text_for_page = "Text from view code"
    context = {
        'text_for_page': text_for_page,
    }
    return render(request, 'sunburst/index.html', context)

def asterank_json(request):
    parser = Parser()
    return HttpResponse(parser.hierJson, content_type='application/json', )