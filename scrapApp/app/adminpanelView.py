from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import AuthUser
from django.contrib import messages

# admin panel control user view


@login_required(login_url='/admin/login/')
def AdminUserList(request):
    title = 'User List'
    data = User.objects.all()
    context = {
        'title': title,
        'data': data,
    }

    return render(request, "admin/adminuser_list.html", context)

# #user ajax delete
# def AdminUserDelete(request, pk):
#     data = User.objects.get(id=pk)
#     data.delete()
#     return redirect(reverse_lazy('authUser'))

# user edit


def AdminUserEdit(request, id):
    title = 'User Edit'
    obj = get_object_or_404(User, id=id)

    form = AuthUser(request.POST or None, instance=obj)
    context = {
        'form': form,
        'title': title,
    }
    if form.is_valid():
        form.save()
        messages.success(request, 'User Updated Successfully')
        return redirect('/admin/user')

    return render(request, 'admin/adminuser_edit.html', context)

# user view


def AdimUserView(request, id):
    title = 'User Edit'
    if request.method == "GET":
        display = User.objects.get(id=id)
    return render(request, "admin/adminuser_view.html", {'title': title, 'display': display})
