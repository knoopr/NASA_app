from django.shortcuts import render
from django.http import HttpResponse
# from sunburst.Backend_parsing import Parser
import json

def index(request):
    text_for_page = "Text from view code"
    context = {
        'text_for_page': text_for_page,
    }
    return render(request, 'sunburst/index.html', context)

def asterank_json(request):
        # TODO Fix, this is lazy
    try:
        # Path on heroku
        with open("neovi/sunburst/static/sunburst/json/Parser_Output_specOuter.txt", "r") as fp:
            json_Data = json.load(fp)
    except FileNotFoundError:
        # Path on localhost
        with open("sunburst/static/sunburst/json/Parser_Output_specOuter.txt", "r") as fp:
            json_Data = json.load(fp)
    return HttpResponse(json.dumps(json_Data, indent=1, separators=(',', ': ')), content_type='application/json', )