import pandas as pd
from sklearn.model_selection import train_test_split
from PIL import Image
from ResponseDto import ResponseDto
import os
import zipfile
import shutil


unzip_path = 'unzipped_data/'
temp_path = 'temp_data/'
temp_images_path = 'temp_data/images/'
images_path = 'unzipped_data/images/'
finished_path = 'finished_data/'


class Configurator():
    os.makedirs(unzip_path, exist_ok=True)
    os.makedirs(temp_path, exist_ok=True)
    os.makedirs(images_path, exist_ok=True)
    os.makedirs(temp_images_path, exist_ok=True)
    os.makedirs(finished_path, exist_ok=True)
        
    def __init__(self):
        pass

    def train_test(self, zip_file, image_dimensions=(128, 128), grayscale=False, structure="inferred"):
        responseDto = ResponseDto("train/test")

        try:
            self.unzip_data(zip_file)
            self.preprocess_images(image_dimensions, grayscale)
            self.split_data_train_test()
            self.inferr_structure(structure)
            self.zip_data()
            self.cleanup()
        except:
            return responseDto.FAILURE
        
        return responseDto.SUCCESS


    def train_val_test(self, zip_file, image_dimensions=(128, 128), grayscale=False, structure="inferred"):
        responseDto = ResponseDto("train/val/test")

        try:
            self.unzip_data(zip_file)
            self.preprocess_images(image_dimensions, grayscale)
            self.split_data_train_val_test()
            self.inferr_structure(structure)
            self.zip_data()
            self.cleanup()
        except Exception as e:
            print(e)
            return responseDto.FAILURE
        
        return responseDto.SUCCESS



        
    def unzip_data(self, zip_file):
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
            


    def split_data_train_test(self, train_size=0.8):
        df = pd.read_csv(os.path.join(unzip_path, 'labels.csv'))
        train, test = train_test_split(df, test_size=1-train_size)
        train.to_csv('finished_data/train.csv', index=False)
        test.to_csv('finished_data/test.csv', index=False)
        return train, test


    def split_data_train_val_test(self, train_size=0.8, val_size=0.15, test_size=0.15):
        df = pd.read_csv(os.path.join(unzip_path, 'labels.csv'))
        train, temp = train_test_split(df, test_size=0.3)
        val, test = train_test_split(temp, test_size=0.5)
        train.to_csv('finished_data/train.csv', index=False)
        val.to_csv('finished_data/val.csv', index=False)
        test.to_csv('finished_data/test.csv', index=False)
        print("successfully split training, dev and test data")
        return train, val, test

    def inferr_structure(self, structure):
        if structure == "inferred":
            train_df = pd.read_csv('finished_data/train.csv')
            for label in train_df['class'].unique():
                os.makedirs(os.path.join(finished_path + "train/", str(label)), exist_ok=True)
            for index, row in train_df.iterrows():
                copies =  shutil.copy(os.path.join(temp_images_path, row["image"]), os.path.join(finished_path + "train/", str(row["class"]), row["image"]))

            test_df = pd.read_csv('finished_data/test.csv')
            for label in test_df['class'].unique():
                os.makedirs(os.path.join(finished_path + "test/", str(label)), exist_ok=True)
            for index, row in test_df.iterrows():
                copies =  shutil.copy(os.path.join(temp_images_path, row["image"]), os.path.join(finished_path + "test/", str(row["class"]), row["image"]))
            
            try:
                val_df = pd.read_csv('finished_data/val.csv')
                for label in val_df['class'].unique():
                    os.makedirs(os.path.join(finished_path + "val/", str(label)), exist_ok=True)
                for index, row in val_df.iterrows():
                    copies =  shutil.copy(os.path.join(temp_images_path, row["image"]), os.path.join(finished_path + "val/", str(row["class"]), row["image"]))
            except:
                print("No validation data")


            else:
                for label in train_df['class'].unique():
                    os.makedirs(os.path.join(temp_path, str(label)), exist_ok=True)
                for index, row in train_df.iterrows():
                    copies =  shutil.copy(os.path.join(temp_images_path, row["image"]), os.path.join(temp_path, str(row["class"]), row["image"]))
            
    


    def preprocess_images(self,dimensions, grayscale=False ):
        x, y = dimensions
        for image in os.listdir(images_path):
            img = Image.open(images_path + image)
            img.resize((int(x), int(y)), Image.Resampling.LANCZOS)
            #convert to grayscale
            if grayscale and img.mode != 'L':
                img = img.convert('L')
            img.save(temp_images_path + image)


    def zip_data(self):
        shutil.make_archive('restructured_data', 'zip', finished_path)


    def cleanup(self):
        shutil.rmtree(images_path)
        shutil.rmtree(unzip_path)
        shutil.rmtree(temp_path)
        shutil.rmtree(finished_path)

