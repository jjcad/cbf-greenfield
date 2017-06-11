import os

from watson_developer_cloud import VisualRecognitionV3

class PlantWhisperer():

    def __init__(self, visual_recognition_key, image):
        """
        Creates a new instance of HealthBot.
        Parameters
        ----------
        visual_recognition_key - The Watson Visual Recognition API Key
        visual_recognition_url - The Watson Visual Recognition API Endpoint
        """
        #self.user_store = user_store
        #self.dialog_store = dialog_store
        self.visual_recognition_client = VisualRecognitionV3(
            api_key=visual_recognition_key,
            version='2016-05-20'
        )
        self.image = os.path.abspath(image)

    def send_image_to_be_classified(self):
        """
        Sends the image to the classifier.
        """
        with open(self.image, 'rb') as f:
            output=self.visual_recognition_client.classify(
                images_file=f,
                classifier_ids=['plant_1358867931'],
                threshold=0.0001
            )

        return output
