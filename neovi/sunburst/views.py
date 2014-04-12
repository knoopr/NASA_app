from django.shortcuts import render
from django.http import HttpResponse
import json

def index(request):
    text_for_page = "Text from view code"
    context = {
        'text_for_page': text_for_page,
    }
    return render(request, 'sunburst/index.html', context)

def asterank_json(request):
    with open("sunburst/static/sunburst/txt/qlt5pn3.txt", "r") as fp:
        json_Data = json.load(fp)
        return HttpResponse(json_Data, mimetype='application/json')