import os
import random
import shutil

def split_data(source_dir, train_dir, val_dir, split_ratio=0.8):
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)
    for class_name in os.listdir(source_dir):
        class_path = os.path.join(source_dir, class_name)
        if os.path.isdir(class_path):
            images = os.listdir(class_path)                                    
            random.shuffle(images)  
            train_count = int(len(images) * split_ratio)    

            class_train_dir = os.path.join(train_dir, class_name)
            class_val_dir = os.path.join(val_dir, class_name)
            os.makedirs(class_train_dir, exist_ok=True)
            os.makedirs(class_val_dir, exist_ok=True)      

            for i, image in enumerate(images):     
                src = os.path.join(class_path, image)
                if i < train_count:
                    dest = os.path.join(class_train_dir, image)
                else:
                    dest = os.path.join(class_val_dir, image)
                shutil.copyfile(src, dest)

if __name__ == "__main__":
    data_dir = "D:\MModel\dataset"
    train_dir = "dataset_split/train"
    val_dir = "dataset_split/val"
    split_data(data_dir, train_dir, val_dir)