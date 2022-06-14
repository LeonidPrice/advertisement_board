from ast import Return, keyword
from multiprocessing import context
from re import template
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import AdvUser
from .forms import ChangeUserInfoForm
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.edit import CreateView
from .forms import RegisterUserForm
from django.views.generic.base import TemplateView
from django.core.signing import BadSignature
from .utilities import signer
from django.views.generic.edit import DeleteView
from django.contrib.auth import logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import SubRubric, Board
from .forms import SearchForm

def index(request):
    return render(request, 'main/index.html')

def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))

class BLoginView(LoginView):
    template_name = 'main/login.html'

@login_required
def profile(request):
    return render(request, 'main/profile.html')

class BLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'
# LoginRequiredMixin добавлен по тому что страница выхода доступна только зарегистрирванным пользователям

class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Данные пользователя изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)
    # получение ключа текущего пользователя

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
    # извлечение исправляемой записи

class BPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменен'
    # смена пароль пользователя

class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')
    # класс регистрирующий пользователя

class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'
    # вывод сообщения об успешной активации

def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active =True
        user.is_activated = True
        user.save()
    return render(request, template)
    # проверка активации

class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)
        # сохранение ключа текущего пользователя

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удалён')
        return super().post(request, *args, **kwargs)
        # выход, всплывающее сообщение об удалении

    def get_object(self,queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
        # поиск по ключу из setup пользователя подлежащего удалению

def by_rubric(request, pk):
    rubric = get_object_or_404(SubRubric, pk=pk)
    boards = Board.objects.filter(is_active=True, rubric=pk)

    # фильтрация объявлений по поисковому запросу
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        boards = boards.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword':keyword}) # для вывода на экран
    paginator = Paginator(boards,2) # 2 - количество записей для проверки пагинатора
    if 'page' in request.GET:
        page_number = request.GET['page']
    else:
        page_number = 1
    page = paginator.get_page(page_number)
    context = {'rubric': rubric,
        'page': page,
        'boards': page.object_list,
        'form': form}
    return render(request, 'main/by_rubric.html', context)

def detail(request, rubric_pk, pk):
    board = get_object_or_404(Board, pk=pk)
    ais = board.additionalimage_set.all() # дополнительные иллюстрации
    context = {'board': board, 'ais': ais}
    return render(request, 'main/detail.html', context)
