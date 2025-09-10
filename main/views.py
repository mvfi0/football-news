from django.shortcuts import render, redirect, get_object_or_404
from main.forms import NewsForm
from main.models import News
from django.http import HttpResponse, Http404
from django.core import serializers

def show_main(request):
    news_list = News.objects.all()

    context = {
        'npm' : '240123456',
        'name': 'Haru Urara',
        'class': 'PBP A',
        'news_list': news_list
    }

    return render(request, "main.html", context)

def create_news(request):
    form = NewsForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_news.html", context)

def show_news(request, id):
    news = get_object_or_404(News, pk=id)
    news.increment_views()

    context = {
        'news': news
    }

    return render(request, "news_detail.html", context)

def show_xml(request):
    data = News.objects.all()
    xml_data = serializers.serialize("xml", data)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    news_list = News.objects.all()
    json_data = serializers.serialize("json", news_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request, news_id):
    qs = News.objects.filter(pk=news_id)   # queryset for serialize()
    if not qs.exists():
        raise Http404("News not found")
    return HttpResponse(
        serializers.serialize("xml", qs),
        content_type="application/xml",
    )

def show_json_by_id(request, news_id):
    obj = get_object_or_404(News, pk=news_id)   # single object
    return HttpResponse(
        serializers.serialize("json", [obj]),    # wrap in list
        content_type="application/json",
    )