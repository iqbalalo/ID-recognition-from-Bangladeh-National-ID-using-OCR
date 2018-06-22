import os
from tesserocr import PyTessBaseAPI
from PIL import Image
from scipy.misc import imsave
import numpy
import re
import locale

locale.setlocale(locale.LC_ALL, "C")

img1 = Image.open('test.jpg')

def convert_to_black_n_white(img, threshold):
    t_img = img.convert('L')
    t_img = numpy.asarray(t_img)
    t_data = (t_img > threshold) * 1.0

    # t_img = numpy.array(t_img)
    # t_img = binarize_array(t_img, threshold)
    imsave("bw_image.jpg", t_data)
    t_img = Image.open('bw_image.jpg')

    t_img.show()
    get_text_from_image(t_img)


def get_text_from_image(img):
    # tessdata path may different in your environment
    with PyTessBaseAPI(path='/usr/local/Cellar/tesseract/3.05.02/share/tessdata', lang='eng+ben') as api:
        api.SetVariable("load_system_dawg", 'T')
        api.SetVariable("load_freq_dawg", 'T')
        api.SetImage(img)
        text = api.GetUTF8Text()

        t_bd_signature = re.search("Republic of Bangladesh", text)
        t_nid_title = re.search("NATIONAL ID", text)
        t_name = re.search("Name:[\w\s,.]+", text)
        t_nid = re.search("ID NO:[ \d \"\[.+\]\" ' ]+", text)

        if t_bd_signature:
            t_bd_signature = t_bd_signature.group(0)

        if t_nid_title:
            t_nid_title = t_nid_title.group(0)

        if t_name:
            t_name = t_name.group(0).split(":")
            t_name = t_name[1].strip()

        if t_nid:
            t_nid = t_nid.group(0)
            t_nid = re.findall(r'\d+', t_nid)
            t_nid = ''.join(t_nid)
        else:
            print("Error! Try again.")

        print(t_bd_signature)
        print(t_nid_title)
        print(t_name)
        print(t_nid)

convert_to_black_n_white(img1, 160)
