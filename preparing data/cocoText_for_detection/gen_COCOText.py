import os
import json
import cv2
import shutil


def read_json(json_file_path:str) -> dict:
  """
  Read Json file from the parameter 'jsons_file_path' and load the content in a data dict.

  Args : 
    - json_file_path : string, path to the json file.
  """
  f = open(json_file_path)
  data = json.load(f)
  f.close()
  return data


def extarct_images_and_ids(data:dict) -> dict:
    """
    Extract the names and ids of images from data extracted from the json file.
    Results are stored in a dict.
    The keys are the names of the images.
    The values are the ids.

    Args : 
     - data : dictionary that contains the annotation data.
    """
    images = {}
    img_keys = list(data["imgs"])

    for im in img_keys:
        images[data["imgs"][im]["file_name"]]=str(data["imgs"][im]['id'])
    return images


def get_bboxes(img_id:int, data:dict) -> list:
    """
    Find the bounding boxes of a text from the image having the given id.
    Results are stored in a list.

    Args : 
     - img_id : int, id of the image extracted from the annotation file. 
     - data : dictionary that contains the annotation data.
    """
    bboxes = []
    ann_keys = data["imgToAnns"][img_id]
    for key in ann_keys:
        ann_id = str(key)
        if (data["anns"][ann_id]["image_id"]== int(img_id)) and (data["anns"][ann_id]['legibility']=='legible'):    
            bboxes.append(data["anns"][str(key)]["bbox"])
    return bboxes

def gen_labels(json_file_path:str,images_src:str, images_dest:str, output_path:str) -> None:
    """
    Generate an annotation file in txt format for each images.
    Each line contains the class and the bounding box of a detected object.
    For each images in the source directory, the image id is extracted (using the extract_images_and_ids function), as well as the bouding boxes.
    If the image contains text, a copy is made in the images_dest directory and the bounding boxes are converted in the yolo format and normalized.

    Args : 
     - json_file_path : string, path to the json file.
     - images_src : string, path to the directory containing the images to be annotated.
     - images_dest : string, path to the directory where the images with text will be copied.
     - output_path : string, path to the destination of the text annotation files. 
    
    """
    data = read_json(json_file_path) 
    images = extarct_images_and_ids(data)
    count = 0 
    for file in os.listdir(images_src):
        if file in list(images.keys()):
            print(file)
            file_id = images[file]
            file_bboxes = get_bboxes(file_id,data)
            if (len(file_bboxes) > 0) : 
                shutil.copyfile(images_src+"/"+file, images_dest+"/"+file)

                # Getting images width and height 
                img_path = os.path.join(images_src, file)
                img = cv2.imread(img_path)
                img_h, img_w = img.shape[:2]
                for current_bbox in file_bboxes : 
                    x = current_bbox[0]
                    y = current_bbox[1]
                    w = current_bbox[2]
                    h = current_bbox[3]
                    
                    # Finding midpoints
                    x_centre = (x + (x+w))/2
                    y_centre = (y + (y+h))/2
                        
                    # Normalization
                    x_centre = x_centre / img_w
                    y_centre = y_centre / img_h
                    w = w / img_w
                    h = h / img_h

                    category = 32
                    
                # Generate text file 
            
                ann_file_path = os.path.join(output_path,file.replace(".jpg",".txt"))
                f = open(ann_file_path, "x")
                f.write(f"{category} {x_centre} {y_centre} {w} {h}\n")
                count += 1 
                print("file"+str(count)+"  generated")
            else : print("no text in the image")
  


