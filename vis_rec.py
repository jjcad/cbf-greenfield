import os

from watson_developer_cloud import VisualRecognitionV3

class PlantWhisperer():

    def __init__(self, visual_recognition_key):
        """
        Creates a new instance of HealthBot.
        Parameters
        ----------
        visual_recognition_key - The Watson Visual Recognition API Key
        image - The file path of the file to be classified.
        """
        #self.user_store = user_store
        #self.dialog_store = dialog_store
        self.visual_recognition_client = VisualRecognitionV3(
            api_key=visual_recognition_key,
            version='2016-05-20'
        )

    def send_imageFile_to_be_classified(self, image):
        """
        Sends the image to the classifier.
        """
        with open(image, 'rb') as f:
            output=self.visual_recognition_client.classify(
                images_file=f,
                classifier_ids=['plant_1358867931'],
                threshold=0.0001
            )

        return output

    def send_imageUrl_to_be_classified(self, image):
        """
        Sends the image to the classifier.
        """
        output = self.visual_recognition_client.classify(
            images_url=image,
            classifier_ids=['plant_1358867931'],
            threshold=0.0001
        )

        return output

    def is_plant_healthy(self, image):
        """
        Returns the class with the highest score.
        """
        if os.path.isfile(image):
            image = os.path.abspath(image)
            obj = self.send_imageFile_to_be_classified(image)
        else:
            obj = self.send_imageUrl_to_be_classified(image)

        classes = obj['images'][0]['classifiers'][0]['classes']
        l = [(x['class'], x['score']) for x in classes]
        l.sort(key=lambda x: -x[1])

        winner = l[0]
        
        return(winner[0])
