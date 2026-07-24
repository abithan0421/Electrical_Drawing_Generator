import os
import cv2
import shutil

def load_images_from_folder(folder, dimension):
    input_folder = folder
    directory = folder.split("/")
    output_folder = "processed_floor_plans/" + directory[-2] + "/" + "images/"

    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if(filename.endswith((".jpg", ".jpeg", ".png"))):
            img_path = os.path.join(input_folder, filename)
            img = cv2.imread(img_path)

            resized_img = cv2.resize(img, (dimension, dimension))

            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, resized_img)

    input_folder_label = directory[0] + '/' + directory[-2] + '/' + 'labels/'
    output_folder_label = 'processed_floor_plans/' + directory[-2] + '/' + 'labels/'

    os.makedirs(output_folder_label, exist_ok=True)
    shutil.copytree(input_folder_label, output_folder_label, dirs_exist_ok=True)

def flush():
    shutil.rmtree("processed_floor_plans/", ignore_errors=True)
    
