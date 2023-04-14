import os
import random
import shutil


def split(num:int, imgs_src:str, anns_src:str ,imgs_dest:str, anns_dest:str) -> None:
  """
  'Num' is the number of samples to be moved from train folder to val folder.
  For the given number of samples, a random images is selected, as well as the correspondant text file annotation.
  Both files are moved to the images destination(imgs_dest) and annotations destination (anns_dest).

  """
  for i in range(num):
    random_img=random.choice(os.listdir(imgs_src))
    ann_file_name = random_img.replace("jpg","txt")
    ann_file_src = os.path.join(anns_src, ann_file_name)
    img_src = os.path.join(imgs_src, random_img)
    img_dest = os.path.join(imgs_dest,random_img)
    ann_file_dest = os.path.join(anns_dest,ann_file_name)
    shutil.move(img_src,img_dest)
    shutil.move(ann_file_src,ann_file_dest)
    print("sample "+str(i)+"/"+str(num)+" moved successfully")