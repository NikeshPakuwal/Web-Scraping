from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import auth, messages
from django.contrib.auth.decorators import permission_required
from django.urls import reverse_lazy
from .forms import CreateUserForm
from django.views import View
from .models import Semrush
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datatables_view.views import DatatablesView
from django.contrib import messages
import io
import csv


# Create your views here.
@login_required(login_url='/admin/login/')
@permission_required('auth.view_user')
def backend_home(request):
    title = 'Dashboard'
    context = {
        'title': title
    }
    return render(request, 'admin/home.html', context)


@login_required(login_url='/admin/login/')
def RedirectView(request):
    return render(request, 'admin/auth/login.html')


@login_required(login_url='/admin/login/')
def user_pending(request):
    title = 'User Pending'
    context = {
        'title': title
    }
    return render(request, 'admin/pending.html', context)


def backend_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user:
            if user.is_active:
                if user.is_staff:
                    login(request, user)
                    return redirect('/admin/')
                else:
                    login(request, user)
                    return redirect('user_pending')
            else:
                # return HttpResponse("")
                messages.error(request, 'Your account was inactive.')
        else:
            messages.error(request, 'Error wrong username/password')

    return render(request, 'admin/auth/login.html')


def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')


def forget_password(request):
    return render(request, 'admin/auth/forget-pass.html')


def user_Register(request):
    title = "Admin Register"
    form = CreateUserForm()
    if request.method == 'POST':

        form = CreateUserForm(request.POST)
        if form.is_valid():

            user = form.save()
            user.refresh_from_db()

            first_name = form.cleaned_data.get('first_name')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')

        else:
            form = CreateUserForm()

    context = {
        'form': form,
        'title': title,
    }
    return render(request, 'admin/auth/register.html', context)


def signup_view(request):
    form = CreateUserForm(request.POST)
    if form.is_valid():
        return redirect('home')
    return render(request, 'signup.html', {'form': form})


class SemrushUploadView(View):
    def get(self, request):
        title = 'Semrush Upload'
        context = {
            'title': title
        }
        template_name = 'admin/semrush/add.html'
        return render(request, template_name, context)

    def post(self, request):
        user = request.user  # get the current login user details
        paramFile = io.TextIOWrapper(request.FILES['semrushfile'].file)
        uploadCSV = csv.DictReader(paramFile)
        list_of_dict = list(uploadCSV)

        objs = [
            Semrush(
                country=row['country'],
                keyword=row['keyword'],
                seed_keyword=row['seed_keyword'],
                tags=row['tags'],
                volume=row['volume'],
                keyword_difficulty=row['keyword_difficulty'],
                ccp=row['ccp'],
                competitive_density=row['competitive_density'],
                number_of_results=row['number_of_results'],
                trend=row['trend'],
                click_potential=row['click_potential'],
                competitors=row['competitors'],
            )
            for row in list_of_dict
        ]
        try:
            msg = Semrush.objects.bulk_create(objs)
            context = {
                'message': messages.success(request, 'Your Semrush Data has been successfully uploaded.')
            }

        except Exception as e:
            # print('Error While Importing Data: ', e)

            context = {
                'message': messages.error(request, 'Your Semrush Data has been something wrong!')
            }

        # return JsonResponse(returnmsg)

        template_name = 'admin/semrush/list.html'
        return render(request, template_name, context)


class SemrushList(View):

    def get(self, request):
        title = 'Semrush Data List'
        context = {
            'title': title,
        }
        template_name = 'admin/semrush/list.html'
        return render(request, template_name, context)


@method_decorator(login_required, name='dispatch')
class SemrushDatatablesView(DatatablesView):
    model = Semrush
    title = 'Semrush'

    column_defs = [
        {
            'name': 'id',
        }, {
            'name': 'country',
        }, {
            'name': 'keyword',
        }, {
            'name': 'seed_keyword',
        }, {
            'name': 'volume',
        }, {
            'name': 'keyword_difficulty',
        }, {
            'name': 'ccp',
        }, {
            'name': 'competitive_density',
            'visible': False,
        },
        {
            'name': 'Action',
            'searchable': False
        }
    ]

    def customize_row(self, row, obj):
        row['country'] = '<b>%s</b>' % obj.country
        row['keyword'] = obj.keyword
        # row['Action'] = '<a href="/%s" class="btn btn-primary"><i class="fas fa-pen"></i></a>' % obj.id
        row[
            'Action'] = '<a class="btn btn-primary" href="%s">%s</a> <a data-url="%s" class="btn btn-danger delete_button">%s</a>' % (
            reverse_lazy('get_links', args=(obj.keyword, obj.id)),
            'Get Link',
            reverse_lazy('semrush_delete', args=(obj.id,)),
            '<i class="fas fa-trash-alt"></i>'
        )

        return


def SemrushListDelete(request, pk):
    data = Semrush.objects.get(id=pk)
    data.delete()
    return redirect(reverse_lazy('semrush'))
