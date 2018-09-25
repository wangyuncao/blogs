from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from backweb.models import Article, Atype


def index(request):
    if request.method == 'GET':
        keyboard = request.GET.get('keyboard', '')
        page_num = int(request.GET.get('page', 1))
        if not keyboard:
            artsdr = Article.objects.filter(a_conceal=False)
        else:
            artsdr = Article.objects.filter(Q(a_name__contains=keyboard) | Q(a_content__contains=keyboard) & Q(a_conceal=False))

        paginator = Paginator(artsdr, 5)
        arts2 = paginator.page(page_num)

        arts1 = Article.objects.filter(a_conceal=False)
        artsd = Article.objects.filter(a_conceal=False).order_by('-a_hit')
        atys = Atype.objects.all()
        for aty in atys:
            aty.count = Article.objects.filter(a_category_id=aty.id, a_conceal=False).count()
        return render(request, 'web/index.html', {'arts1': arts1,
                                                  'arts2': arts2,
                                                  'artsd': artsd,
                                                  'atys': atys,
                                                  'keyboard': keyboard})


def index2(request):
    if request.method == 'GET':
        page_num = int(request.GET.get('page', 1))
        id = request.GET.get('type')
        artsdr = Article.objects.filter(a_conceal=False, a_category_id=id)
        paginator = Paginator(artsdr, 5)
        arts2 = paginator.page(page_num)

        arts1 = Article.objects.filter(a_conceal=False)
        artsd = Article.objects.filter(a_conceal=False).order_by('-a_hit')
        atys = Atype.objects.all()
        for aty in atys:
            aty.count = Article.objects.filter(a_category_id=aty.id, a_conceal=False).count()
        atyd = Atype.objects.get(id=id)
        return render(request, 'web/index2.html', {'arts1': arts1,
                                                   'arts2': arts2,
                                                   'artsd': artsd,
                                                   'atys': atys,
                                                   'atyd': atyd})


def about(request):
    if request.method == 'GET':
        arts1 = Article.objects.filter(a_conceal=False)
        artsd = Article.objects.filter(a_conceal=False).order_by('-a_hit')
        atys = Atype.objects.all()
        for aty in atys:
            aty.count = Article.objects.filter(a_category_id=aty.id, a_conceal=False).count()
        return render(request, 'web/about.html', {'arts1': arts1,
                                                  'artsd': artsd,
                                                  'atys': atys})


def article(request, id):
    if request.method == 'GET':
        a = Article.objects.filter(id=id)
        a.update(a_hit=a[0].a_hit + 1)
        a = Article.objects.get(id=id)
        arts1 = Article.objects.filter(a_conceal=False)
        artsd = Article.objects.filter(a_conceal=False).order_by('-a_hit')
        atys = Atype.objects.all()
        for aty in atys:
            aty.count = Article.objects.filter(a_category_id=aty.id, a_conceal=False).count()
        return render(request, 'web/article.html', {'a': a,
                                                    'arts1': arts1,
                                                    'artsd': artsd,
                                                    'atys': atys})