from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.


def ani(request):
    if 'log_user' in request.session:
        return render(request, 'upload.html', {'name': request.session['log_user']})
    return redirect('login')