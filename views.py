"""
    Django Photo Gallery Justin Fuhrmeister-Clarke, a photo gallery based in django.
    Copyright (C) 2017  Justin Fuhrmeiser-Clarke <justin@fuhrmeister-clarke.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    """

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect,FileResponse,HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.core.files import File


import mimetypes

from .resize import createPreview, createThumbnail


# Create your views here.


from .models import Photo, Tag, Page
from .forms import *

def getTitle(title=False):
    if(title):
        return getTitle() + " - " + title
    else:
        return "Justin Fuhrmeister-Clarke"

def index(request):
    context = {'title':getTitle(), 'request': request}
    return render(request, 'photos/index.html', context)

def login(request):
    context = {'title':getTitle(), 'request': request}
    return render(request, 'photos/login.html', context)

def logout(request):
    return HttpResponseRedirect(reverse('photos:index'))

def admin_list(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('photos:index'))
    photos = Photo.objects.all().order_by('title')
    tags = Tag.objects.all().order_by('title')
    pages = Page.objects.all().order_by('title')
    navs = Nav.objects.all().order_by('title')

    context = {'title':getTitle(), 'request': request,'photos':photos,'tags':tags,'pages':pages,'navs':navs}
    return render(request, 'photos/admin_list.html', context)


def add(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('photos:index'))
        
    if request.method == "POST":
        photo = PhotoForm(request.POST, request.FILES) # A form bound to the POST data
        if photo.is_valid(): # All validation rules pass
            new_photo = photo.save()

            #resize image for thumbnail and preview
            photo = Photo.objects.get(pk=new_photo.id)
            photo.preview_file = createPreview(photo.image_file.name,'photo_files/previews/')
            photo.thumbnail_file = createThumbnail(photo.image_file.name,'photo_files/thumbnails/')
            photo.save()
            #end resize
            
            return HttpResponseRedirect(reverse('photos:admin_list'))
    else:
        photo = PhotoForm()
    context = {'title':getTitle(), 'request': request,'form':photo,'id':'0'}
    return render(request, 'photos/add.html', context)



def edit(request,id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('photos:index'))
    photo = get_object_or_404(Photo, pk=id)
    if request.method == "POST":
        photo = PhotoForm(request.POST) # A form bound to the POST data
        if photo.is_valid(): # All validation rules pass
            new_photo = photo.save()
            #resize image for thumbnail and preview
            photo = Photo.objects.get(pk=new_photo.id)
            photo.preview_file = createPreview(photo.image_file.name,'photo_files/previews/')
            photo.thumbnail_file = createThumbnail(photo.image_file.name,'photo_files/thumbnails/')
            photo.save()
            #end resize
            return HttpResponseRedirect(reverse('photos:admin_list'))
    else:
        tags_data = photo.tags.values()
        tags=[]
        for tag in tags_data:
            tags.append(tag['id'])
        data ={
        'title':photo,
        'capture_date':photo.capture_date,
        'description':photo.description,
        #'tags':tags,
        'tags':photo.tags.values_list('id',flat=True),
        'image_file':photo.image_file.name,
        }
        photo = PhotoForm(data)
    context = {'title':getTitle(), 'request': request,'form':photo,'id':id}
    return render(request, 'photos/add.html', context)
    
    
    
def add_tag(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('photos:index'))
    if request.method == "POST":
        tag = TagForm(request.POST) # A form bound to the POST data
        if tag.is_valid(): # All validation rules pass
            new_tag = tag.save()
            return HttpResponseRedirect(reverse('photos:admin_list'))
    else:
        tag = TagForm()
    context = {'title':getTitle(), 'request': request,'form':tag}
    return render(request, 'photos/add.html', context)
    
def edit_tag(request,id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('photos:index'))
    tag = get_object_or_404(Tag, pk=id)
    if request.method == "POST":
        tag = TagForm(request.POST) # A form bound to the POST data
        if tag.is_valid(): # All validation rules pass
            new_tag = tag.save()
            return HttpResponseRedirect(reverse('photos:admin_list'))
    else:
        data={
            'title':tag.title,
        }
        tag = TagForm(data)
    context = {'title':getTitle(), 'request': request,'form':tag}
    return render(request, 'photos/add.html', context)



def view_single(request,id):
    photo = get_object_or_404(Photo, pk=id)
    context = {'title':getTitle(), 'request': request,'photo':photo}
    return render(request, 'photos/view_single.html', context)

def view_all(request):
    photos = Photo.objects.all().order_by('title')
    context = {'title':getTitle(), 'request': request,'photos':photos}
    return render(request, 'photos/view_all.html', context)



def preview(request,id):
    photo = get_object_or_404(Photo, pk=id)
    
    return HttpResponse(content=FileResponse(open(photo.preview_file.name, 'rb')),content_type=mimetypes.guess_type(photo.preview_file.name)[0])
    #return FileResponse(open(photo.preview_file.name, 'rb'))
    

def thumbnail(request,id):
    photo = get_object_or_404(Photo, pk=id)
    #photo_file = open(photo.image_file)
    #return FileResponse(photo.image_file.open())
    #return HttpResponse(content=FileResponse(open(photo.image_file.name, 'rb')),content_type=mimetypes.guess_type(photo.image_file.name)[0])
    return HttpResponse(content=FileResponse(open(photo.thumbnail_file.name, 'rb')),content_type=mimetypes.guess_type(photo.thumbnail_file.name)[0])

def original(request,id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("No Access")
    photo = get_object_or_404(Photo, pk=id)
    #photo_file = open(photo.image_file)
    #return FileResponse(photo.image_file.open())
    return HttpResponse(content=FileResponse(open(photo.image_file.name, 'rb')),content_type=mimetypes.guess_type(photo.image_file.name)[0])
    #return FileResponse(open(photo.image_file.name, 'rb'))
    #return HttpResponse(content=FileResponse(open(photo.thumbnail_file.name, 'rb')),content_type=mimetypes.guess_type(photo.thumbnail_file.name)[0])


def add_page(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('photos:index'))
    if request.method == "POST":
        page = PageForm(request.POST) # A form bound to the POST data
        if page.is_valid(): # All validation rules pass
            new_page = page.save()
            return HttpResponseRedirect(reverse('photos:admin_list'))
    else:
        page = PageForm()
    context = {'title':getTitle(), 'request': request,'form':page}
    return render(request, 'photos/add.html', context)
    
def edit_page(request,id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('photos:index'))
    page = get_object_or_404(Page, pk=id)
    if request.method == "POST":
        page = PageForm(request.POST) # A form bound to the POST data
        if page.is_valid(): # All validation rules pass
            new_page = page.save()
            return HttpResponseRedirect(reverse('photos:admin_list'))
    else:
        data={'title':page.title,
            'url':page.url,
            'content':page.content,
        }
        page = PageForm(data)
    context = {'title':getTitle(), 'request': request,'form':page}
    return render(request, 'photos/add.html', context)

def page(request,url_var):
    
    page_var = get_object_or_404(Page, url=url_var)

    context = {'title':getTitle(),'request': request,'data':page_var}
    return render(request, 'photos/page.html', context)


def add_nav(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('photos:index'))
    if request.method == "POST":
        nav = NavForm(request.POST) # A form bound to the POST data
        if nav.is_valid(): # All validation rules pass
            new_nav = nav.save()
            return HttpResponseRedirect(reverse('photos:admin_list'))
    else:
        nav = NavForm()
    context = {'title':getTitle(), 'request': request,'form':nav}
    return render(request, 'photos/add.html', context)
    
def edit_nav(request,id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('photos:index'))
    nav = get_object_or_404(Nav, pk=id)
    if request.method == "POST":
        nav = NavForm(request.POST) # A form bound to the POST data
        if nav.is_valid(): # All validation rules pass
            new_nav = nav.save()
            return HttpResponseRedirect(reverse('photos:admin_list'))
    else:
        data={'title':nav.title,
            'url':nav.url,
            'content':nav.content,
        }
        nav = NavForm(data)
    context = {'title':getTitle(), 'request': request,'form':nav}
    return render(request, 'photos/add.html', context)

def reload_previews(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('photos:index'))
    photos = Photo.objects.all().order_by('title')
    for photo in photos:
        #photo = Photo.objects.get(pk=new_photo.id)
        photo.preview_file = createPreview(photo.image_file.name,'photo_files/previews/')
        photo.thumbnail_file = createThumbnail(photo.image_file.name,'photo_files/thumbnails/')
        photo.save()

    return HttpResponseRedirect(reverse('photos:view_all'))

def test(request,id):
    
    context = {'title':getTitle(), 'request': request}
    return render(request, 'photos/test.html', context)
