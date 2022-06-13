from .models import SubRubric

def board_context_processor(request):
    context = {}
    context['rubrics'] = SubRubric.objects.all()
    context['keyword'] = ''
    context['all'] = ''
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            context['keyword'] = '?keyword=' + keyword
            context['all'] = context['keyword']
    if 'page' in request.GET:
        page = request.GET['page']
        if page != '1':
            if context['all']:
                context['all'] += '&page=' + page
            else:
                context['all'] = '?page=' + page
    return context
    # обработчик контекста создающий список подрубрик для объявлений
    # список подрубрик помещается в переменную "rubrics"
    # Необходимо добавить в setings.py > TEMPLATES > context_processors как "main.middlewares.board_context_processor"