import os 
import cv2
import pathlib


def extract_bbox_train(str_line:str, train:bool) -> list:
    """
    Extract bounding box of an object from a given line from an annotation file.
    The coordinates of the bounding boxes are separated with a comma in test files only.When extracting the bounding boxes coordinates, the comams need 
    to be removed.
    A list that contains the bounding box coordinates is returned.

    Args: 
      - str_line : string referring one line in the annotation file.
      - train : Boolean set true if the str_line is extracted from train annotation file, else False.
    """
    bbox = str_line.split()
    bbox.pop()
    if train : 
        return bbox 
    else : 
        for i in range(len(bbox)): 
            aux = bbox[i]
            bbox[i] = aux[:-1]       
        return bbox



def transform_bbox(bbox:list, img_path:str) -> list:
    """
    Transfrom bbox to center_xywh format.
    The resulted x and y represent the center of the bounding box and are calculated from the borders coordinates in bbox arg.
    The results are normalized by division by the height and width of the image.

    Args : 
      - bbox : list that contains the bounding box coordinates in xyxy format.
      - img_path : string that contains the path to the correspondent image.
    """

    img = cv2.imread(img_path)
    img_h, img_w = img.shape[:2]

    x = float(bbox[0])
    y = float(bbox[1])
    w = float(bbox[2]) - x
    h = float(bbox[3]) - y 
          
    x_centre = (x + (x+w))/2
    y_centre = (y + (y+h))/2
          
    x_centre = x_centre / img_w
    y_centre = y_centre / img_h
    w = w / img_w
    h = h / img_h
    res = [x_centre, y_centre, w, h]
    return res 


def gen_lab(images_path:str, gt_src_path:str, output_path:str,train:bool) -> None :
    """
    Generate the text files for each image in the images path directory

    Args : 
      - images_path : String, path to the images to be annotated
      - gt_src_path : string, path to the original annotation files.
      - output_path : string, path to the directory where the new text files will be generated.
      - train : boolean set true if the annotation file belongs to the training set, false otherwise.
    """
    for file in os.listdir(images_path):

        #get img path
        img_path = os.path.join(images_path, file)

        print(file)

        #reading file lines 
        name = str(pathlib.Path(file).with_suffix(".txt"))
        file_path = os.path.join(gt_src_path,"gt_"+name)
        with open(file_path,"r") as f : 
            lines = f.readlines()
        
        #creating new text file
        output_file_path =os.path.join(output_path,name)
        w = open(output_file_path, "w")
        for line in lines :
            if len(line)>2 : 
                bbox =extract_bbox_train(line,train)
                t_bbox = transform_bbox(bbox,img_path)
                label = 32
                w.write(f"{label} {t_bbox[0]} {t_bbox[1]} {t_bbox[2]} {t_bbox[3]}\n")
        print("file generated")


