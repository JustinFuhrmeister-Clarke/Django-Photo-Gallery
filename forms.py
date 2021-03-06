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
from django.forms import ModelForm
from django import forms
from .models import Photo, Tag


# Create the form class.
class PhotoForm(ModelForm):
    description = forms.CharField(widget=forms.Textarea, required=False)
    sales_embed = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Photo
        #fields = '__all__'
        fields = [
        'title',
        'capture_date',
        'description',
        'tags',
        'image_file',
        'sales_embed',
        ]

class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'
        #fields = [ 'Title' ]
