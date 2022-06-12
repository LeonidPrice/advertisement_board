from .models import SubRubric

def board_context_processor(request):
    context = {}
    context['rubrics'] = SubRubric.objects.all()
    return context
    # обработчик контекста создающий список подрубрик для объявлений
    # список подрубрик помещается в переменную "rubrics"
    # Необходимо добавить в setings.py > TEMPLATES > context_processors как "main.middlewares.board_context_processor"