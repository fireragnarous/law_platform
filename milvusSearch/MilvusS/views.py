from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
    return HttpResponse("Hello world")


def runoob(request):
    """
    view: {"HTML变量名":"views变量名"}
    HTML: {{ 变量名}}
    :param request:
    :return:
    """

    context  = {}
    context['DATA_MANAGEMENT'] = 'Omnilab实验室先进数据集数据管理平台'
    context['VIEW_LISTS'] = ['检索结果1','检索结果2','检索结果3','检索结果4']
    return render(request, 'runoob.html', context)

