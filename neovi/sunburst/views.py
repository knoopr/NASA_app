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
    with open("../neovi/sunburst/static/sunburst/json/qlt5pn3.json", "r") as fp:
        json_Data = json.load(fp)
        return HttpResponse(json.dumps(json_Data, indent=1, separators=(',', ': ')), content_type='application/json', )