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
from PIL import Image
import os

import exifread


def getRotate(orientation):
    #print(orientation)
    orientTest=str(orientation)
    #print(orientTest)
    #print("Horizontal (normal)")
    if(orientTest == "Horizontal (normal)"):
        return 0
    if(orientTest == "Rotated 90 CW"):
        return 270
    if(orientTest == "Rotated 90 CCW"):
        return 90
    return 180

def createPreview(inFile,outDir,size=[1280,720]):
    pass
    file, ext = os.path.splitext(inFile)
    title= file.split('/')[-1]
    im = Image.open(inFile)
    
    fRotate = open(inFile, 'rb')
    tags = exifread.process_file(fRotate, stop_tag='Orientation')
    orientation=tags['Image Orientation']
    fRotate.close()
   
    imPreview = im.copy()
    imPreview=imPreview.rotate(getRotate(orientation),expand=1)
    imPreview.thumbnail(size)
    imPreview.save(outDir+"preview-"+title+".jpg","JPEG")
    imPreview.close()
    return outDir+"preview-"+title+".jpg"

def createThumbnail(inFile,outDir,size=[256,128]):
    pass
    file, ext = os.path.splitext(inFile)
    title= file.split('/')[-1]
    im = Image.open(inFile)
    
    fRotate = open(inFile, 'rb')
    tags = exifread.process_file(fRotate, stop_tag='Orientation')
    orientation=tags['Image Orientation']
    fRotate.close()
   
    imThumbnail = im.copy()
    imThumbnail=imThumbnail.rotate(getRotate(orientation),expand=1)
    imThumbnail.thumbnail(size)
    imThumbnail.save(outDir+"thumbnail-"+title+".jpg","JPEG")
    imThumbnail.close()
    
    return outDir+"thumbnail-"+title+".jpg"