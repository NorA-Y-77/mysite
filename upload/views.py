from django.shortcuts import render
from .forms import UploadImageForm
from .models import Image
from .config import AK,SK
from cv2 import cv2

import time
import base64
import requests
import json
import os, sys

def uploadImage(request):
    """图片的上传"""
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            picture = Image(photo=request.FILES['image'])
            picture.save()

            books = imageProcess(picture)
            return render(request, 'upload/showImg.html', {'picture': picture, 'label': books})

    else:
        form = UploadImageForm()

        return render(request, 'upload/uploadform.html', {'form': form})


def imageProcess(picture):
    img = cv2.imread(picture.photo.path)


    #Graying and binarization
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imwrite('gray.jpg',gray)
    ret, binary = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)
    #cv2.imwrite('b.jpg',binary)

    #Corrosion and expansion
    binary = cv2.erode(binary, None, iterations=1)
    #cv2.imwrite('b2.jpg',binary)
    binary = cv2.dilate(binary, None, iterations=1)
    #cv2.imwrite('b3.jpg',binary)

    test, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.imwrite('book.jpg',test )
    #print(contours)
    i = 0
    min_num = 10000
    max_num = 270 * 400
    for contour in contours[1:]:

        x, y, w, h = cv2.boundingRect(contour)
        if (w * h) > min_num:
            if (w * h) < max_num:
                #Draw the whole outline
                out = cv2.rectangle(img,(x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.imwrite('static/media/bookRecognition/first_result.jpg',out)
                i = i + 1
                source = img
                [height, width, pixels] = img.shape  # Extracting original image data
                savimg = source[0:height, x:(x + w)] # Cut image
                cv2.imwrite('static/media/bookRecognition/book{0}.jpg'.format(i), savimg)
                num_book = i
                print('Saved sucessful')
    

   
    access_token = fetch_token()
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # 二进制方式打开图片文件
    
    books = {}

    for n in range(1, num_book+1,1):
        f = open('static/media/bookRecognition/book{0}.jpg'.format(n), 'rb')
        img = base64.b64encode(f.read())
        params = {"image": img}
        request_url = request_url + "?access_token=" + access_token
        headers = {'conten-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        time.sleep(0.5)
        res = json.loads(response.text)
        book = ''
        #book += 'book{0}:\n'.format(n)

        if response:
            for j in res.get('words_result'):
                book += ' '
                book += j.get('words')
                book += ' '
                books['book'+str(n)] = book
                

    return books    

                

API_Key = AK
SECRET_KEY = SK
host = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=24.f9ba9c5241b67688bb4adbed8bc91dec.2592000.1485570332.282335-8574074'
KEY_response = requests.get(host)


# 保证兼容python2以及python3
IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
else:
    pass

# 防止https证书校验不正确
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = 'LsRLpCIMHNGDTFUhNtde1HMO'

SECRET_KEY = '04nqOgMEP0gLtjWnsOHvdBk0GFUKmy6r'


OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"


"""  TOKEN start """
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'


"""
    get token
"""
def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)
    if (IS_PY3):
        result_str = result_str.decode()


    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print ('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print ('please overwrite the correct API_KEY and SECRET_KEY')
        exit()
