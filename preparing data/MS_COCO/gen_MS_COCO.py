import json
import os

# dictionnary to map old categories ids to new ones
new_categories_ids = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:11,
                      16:12, 17:13, 18:14, 19:15, 20:16, 21:17, 22:18, 
                      23:19, 24:20, 25:21 , 35:22, 36:23, 37:24, 39:25,
                      40:26, 41:27, 42:28, 43:29, 62:30, 63:31}

def change_category_id(old_id:int) -> int:
   """
   return the new id correspondent to the old one.
   Args : 
     -old id : int, the id of the category in the original coco annotation.
   """
   return new_categories_ids[old_id]

def read_json(json_file_path:str) -> dict :
  """
  Read Json file from the parameter 'jsons_file_path' and load the content in a data dict.

  Args : 
    - json_file_path : string, path to the json file.
  """
  f = open(json_file_path)
  data = json.load(f)
  f.close()
  return data
   
def get_img(filename:str,data:dict) -> dict:
  """
  Return the dictionary that contains data about image from the annotation data.

  Args : 
   - filename : string, the name of the image.
   - data : dictionary that contains the annotation data.
  """
  for img in data['images']:
    if img['file_name'] == filename:
      return img

def get_img_ann(image_id:int, data:dict) -> list:
    """
    Retrun the annotations of a given image after checking if the image has annotations.

    Args : 
      - image_id : int, the id of the image.
      - data : - data : dictionary that contains the annotation data.
    """
    img_ann = []
    isFound = False
    for ann in data['annotations']:
        if ann['image_id'] == image_id:
            img_ann.append(ann)
            isFound = True
    if isFound:
        return img_ann
    else:
        return None
    
def convert(json_file_path:str, images_path:str, output_path:str) -> None:
  """
  Generate an annotation file in txt format for each images after extracting the annotations from the original annotation file in json format and 
  converting the bounding boxes from xywh format to normalized center_xywh format.

  Args : 
     - json_file_path : string, path to the json file.
     - images_path : string, path to the directory containing the images to be annotated.
     - output_path : string, path to the destination of the text annotation files. 
    
  """
  data = read_json(json_file_path) 
  count = 0 
  categories_ids = list(new_categories_ids.keys())
  for file in os.listdir(images_path):
    img = get_img(file,data)
    img_id = img['id']
    img_w = img['width']
    img_h = img['height']

    # Get Annotations for this image
    img_ann = get_img_ann(img_id,data)

    if img_ann:
      ann_file_name = file.replace("jpg","txt")
      ann_file_path = os.path.join(output_path,ann_file_name)
      f = open(ann_file_path, "x")

      for ann in img_ann:
        if ann['category_id'] not in categories_ids:
           continue 
        else : 
          current_category = change_category_id(ann['category_id']) - 1 # As yolo format labels start from 0 
          current_bbox = ann['bbox']
          x = current_bbox[0]
          y = current_bbox[1]
          w = current_bbox[2]
          h = current_bbox[3]
          
          x_centre = (x + (x+w))/2
          y_centre = (y + (y+h))/2
          
          x_centre = x_centre / img_w
          y_centre = y_centre / img_h
          w = w / img_w
          h = h / img_h
          
          f.write(f"{current_category} {x_centre} {y_centre} {w} {h}\n")
    count += 1  
    print("file "+str(count) + "generated")