import json


class ResponseDto():
    def __init__(self, split=""):
        self.split = split
        self.SUCCESS = self.success()
        self.FAILURE = self.failure()
        self.WRONG_LABELS = self.wrong_labels()


    def success(self):
        return({
            "code": 200,
            "message": f"{self.split} split successfull"
        })
    
    def failure(self):
        return({
            "code": 400,
            "message": f"{self.split} split unsuccessfull, there was a server error, contact Luka M."
        })
    
    def wrong_labels(self):
        return({
            "code": 415,
            "message": f"{self.split} split unsuccessfull, check your label and folder names"
                        "the labels should be 'labels.csv' with 'image' column for filenames, 'class'"
                        "colum for classes and all images should in 'images' folder"
        })
    