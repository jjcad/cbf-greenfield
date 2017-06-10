import json
import sys
import threading

from watson_developer_cloud import VisualRecognitionV3

class PlantWhisperer():

    def __init__(self, visual_recognition_key, visual_recognition_url, image):
        """
        Creates a new instance of HealthBot.
        Parameters
        ----------
        user_store - Instance of CloudantUserStore used to store and retrieve users from Cloudant
        dialog_store - Instance of CloudantDialogStore used to store conversation history
        visual_recognition_key - The Watson Visual Recognition API Key
        visual_recognition_url - The Watson Visual Recognition API Endpoint
        """
        #self.user_store = user_store
        #self.dialog_store = dialog_store
        self.visual_recognition_client = VisualRecognitionV3(
            api_key=visual_recognition_key,
            version='2016-05-20'
        )
        self.image = image

    def init(self):
        """
        Initializes the bot, including the required datastores.
        """
        #self.user_store.init()
        #self.dialog_store.init()

    def send_image_to_be_classified(self):
        """
        Sends the image to the classifier.
        """
        return self.visual_recognition_client.classify(
            images_file=self.image,
            classifier_ids='plant'
        )
