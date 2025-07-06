from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Anime
from django.contrib import messages
# Create your views here.

@login_required
def Upload(request):
    if request.method == "POST":
        title = request.POST.get("title")
        desc = request.POST.get("description")
        img = request.FILES.get("image")
        uploady = request.user

        if title and desc and img:
            Anime.objects.create(title=title, desc=desc, image=img, uploaded_by=uploady)

            #Post/Redirect/Get pattern (PRG) to prevent form resubmission
            messages.success(request, "Anime uploaded successfully!")  #for one timw message showing
            return redirect('UpPage')  # This sends a GET request to /animes/Uppage/
    return render(request,'AniFold/upload.html')



def dashboard(request):
    query = request.GET.get("q")
    if query:
        anime = Anime.objects.filter(title__icontains = query)
    else:
        anime = Anime.objects.all().order_by('-id')
    return render(request, 'dash.html', {'animes' : anime})