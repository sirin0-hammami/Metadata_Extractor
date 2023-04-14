import random
import os 
import cv2
from nltk.corpus import words
from random import sample
import PIL 
from PIL import Image, ImageDraw, ImageFont
import numpy as np 

font_lst = ["Ubuntu-BI.ttf","Ubuntu-C.ttf","Ubuntu-LI.ttf","Ubuntu-L.ttf","Ubuntu-MI.ttf","UbuntuMono-R.ttf","UbuntuMono-BI.ttf","UbuntuMono-RI.ttf"] 


def gen_annotation_file(x:float, y:float, w:float, h:float, img_w:float, img_h:float, file_name:str ,ann_dest:str) -> None:
    """
    Convert the annotation from xywh format to normalized center_xywh format and generate a text file where each line contains the class and the bounding
    box of a detected object.

    Args : 
      - x : float, the left x coordinate of the bounding box.
      - y : floats, the left y coordinate of the bounding box.
      - w : float, the height of the bounding box.
      - h : float, the height of the bounding box.
      - img_h : float, the height of image.
      - img_w : float, the width of the image.
      - file_name : string , name of the text annotation file. 
      - anns_dets : string, path to the destination of the annotation files.
    """
    # Finding midpoints
    x_centre = (x + (x+w))/2
    y_centre = (y + (y+h))/2
                
    # Normalization
    x_centre = x_centre / img_w
    y_centre = y_centre / img_h
    w = w / img_w
    h = h / img_h

    # Generate text file 
    ann_file_path = os.path.join(ann_dest, file_name+".txt" )
    f = open(ann_file_path, "x")
    category = 32
    f.write(f"{category} {x_centre} {y_centre} {w} {h}\n")


def gen_synth_with_bgimg(num:int, imgs_src:str, imgs_dest:str, ann_dest:str) -> None:
    """
    Generate a synthetic text on backgound images.
    At each iteartion, a random image is selected from a given directory. IF the image is bright, a random black text is written over it.

    Args : 
      - num : int, number or iteartions 
      - imgs_src : string, path to the directory of the images.
      - imgs_dest : string, path to directory where the generated images will be saved.
      - ann_dest : string, path to the destination of the annotation files.
    """
    
    for i in range(num):
        try : 
            file = random.choice(os.listdir(imgs_src))
            file_path = os.path.join(imgs_src,file)
            im_r = cv2.imread(file_path)
            gray = cv2.cvtColor(im_r, cv2.COLOR_BGR2GRAY)
            if np.mean(gray) > 50 : 

                img_h, img_w = im_r.shape[:2]
                
                img = Image.open(file_path)
                draw = ImageDraw.Draw(img)

                x = random.randrange(int(img_w/8))
                y = random.randrange(int(img_h/4))

                font_size = random.randrange(15,60)
                fnt = random.choice(font_lst)
                font = ImageFont.truetype(fnt,size=font_size)

                sentence_size= random.randrange(4, 10)
                
                new_sentence =""
                for w in range(sentence_size):
                    new_word = sample(words.words(), 1)[0]
                    test_sentence = new_sentence + "  " + new_word
                    if x + draw.textsize(test_sentence, font=font)[0] > img_w : break
                    else : new_sentence = test_sentence
                
                txt_width, txt_height = draw.textsize(new_sentence, font=font)

                draw.text((x, y), new_sentence, (0,0,0),font=font)

                path = os.path.join(imgs_dest, new_word+".jpg")
                img.save(path)
                    
                gen_annotation_file(x, y, txt_width, txt_height, img_w, img_h, new_word,ann_dest)
        except : 
            continue

