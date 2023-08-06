
from django.urls import path, reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings 
from django import forms 
from django.core.wsgi import get_wsgi_application 
from django.core.cache import cache 
from django.views.decorators.http import etag 
import sys  # Import Sys 
import os 
from io import BytesIO 
from PIL import Image, ImageDraw, ImageFont
import hashlib 


# Settings 
BASE_DIR = os.path.dirname(__file__)
settings.configure(
    DEBUG=True, 
    SECRET_KEY=os.urandom(32),
    ROOT_URLCONF = __name__, 
    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf_CsrfViewMiddleware', 
        'django.middleware.clickjacking.XFrameOptionsMiddleware'
        ),
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.staticfiles',
    ),
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ],
    STATICFILES_DIRS=(
        os.path.join(BASE_DIR, 'static'),
    ),
    STATIC_URL='/static/',
    )


# WSGI Application 
application = get_wsgi_application()

# Forms 
class ImageForm(forms.Form):
    width = forms.IntegerField(min_value=1, max_value=1000)
    height= forms.IntegerField(min_value=1, max_value=1000)
    
    def generate(self, image_format='PNG'):
        width = self.cleaned_data['width']
        height = self.cleaned_data['height']
        key = '{}.{}.{}'.format(width, height, image_format)
        content = cache.get(key)
        if content is None:
            image = Image.new('RGB', (width, height), color=(0, 0, 0))
            draw = ImageDraw.Draw(image)
            text = '{} X {}'.format(width, height)
        
            # You need to define a font and size for the text
            font = ImageFont.truetype('./stocky.ttf', 20)  # Change 'arial.ttf' to the path of your desired font file.
            
            bbox = draw.textbbox((0, 0), text, font=font)
            textwidth = bbox[2] - bbox[0]
            textheight = bbox[3] - bbox[1]
            
            if textwidth < width and textheight < height:
                texttop = (height - textheight) // 2
                textleft = (width - textwidth) // 2
                draw.text((textleft, texttop), text, fill=(255, 255, 255), font=font)
            
            content = BytesIO()
            image.save(content, image_format)
            content.seek(0)
            cache.set(key, content, 3600)
        return content 
    
# Views 
def generate_etag(request, width, height):
    content = 'Placeholder: {0} x {1}'.format(width, height)
    return hashlib.sha1(content.encode('utf-8')).hexdigest()

def index(request):
    example = reverse('placeholder', kwargs={'width': 50, 'height':50})
    context = {
    'example': request.build_absolute_uri(example)
    }
    return render(request, 'index.html', context)

# Placeholder view 
@etag(generate_etag)
def placeholder(request, width, height):
    form = ImageForm({'width': width, 'height' : height})
    if form.is_valid():
        image = form.generate()
        return HttpResponse(image, content_type='image/png')
    else :
        return HttpResponseBadRequest('Invalid Image Request') 
    

# URLS 
urlpatterns = [
    path('', index, name='index'),
    path('image/<int:width>x<int:height>/', placeholder, name='placeholder'), 
]


if __name__ == '__main__':
    from django.core.management import execute_from_command_line 
    
    execute_from_command_line(sys.argv) 
    