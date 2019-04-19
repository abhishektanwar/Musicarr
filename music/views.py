from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .models import Album
from django.http import Http404
from django.contrib.auth import authenticate,login
from django.views.generic import View
from .forms import UserForm

# Create your views here.


def index(request):
    all_albums = Album.objects.all()

    template = loader.get_template('music/index.html')
    context = {
        'all_albums':all_albums,
    }
    return HttpResponse(template.render(context,request))

    '''OR
        return render(request,'music/index.html',context)
    '''
    '''html=''
    for album in all_albums:
        url = '/music/' + str(album.id) + '/'
        html += '<a href=" '+ url +' ">'+ album.album_title +'</a><br>' 
    return HttpResponse(html)'''

def detail(request,album_id):
    try:
        album=Album.objects.get(pk=album_id)
    except Album.DoesNotExist:
        raise Http404("Album does not exist")
    context={'album':album}
    '''template = loader.get_template('music/detail.html')'''
    return render(request,'music/detail.html',context)      
  

def favourite(request,album_id):
    album=Album.objects.get(pk=album_id)  
    try:
        selected_song=album.song_set.get(pk=request.POST['song'])
    except (KeyError,song.DoesNotExist):
        return render(request,'music/detail.html',{
            'album':album,
            'error_message':"You did not select a valid song.",
    })    
    else:
        selected_song.is_favourite=True
        selected_song.save()
        return render(request,'music/detail.html',{'album':album})

class AlbumCreate(CreateView):
    model=Album
    fields=['artist','album_title','genre','logo']

class UserFormView(View):
    form_class=UserForm
    template_name = 'music/registeration_form.html'
    #inbuilt functionality,displays blank form
    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)

            #cleaned normalised data
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('music:index')
        return render(request,self.template_name,{'form':form})
