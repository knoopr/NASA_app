from django.shortcuts import render


def index(request):
    text_for_page = "Text from view code"
    context = {
        'text_for_page': text_for_page,
    }
    return render(request, 'sunburst/index.html', context)