from __future__ import print_function

import threading
import time
from slackclient import SlackClient

class SlackBotController(threading.Thread):

    def __init__(self, health_bot, slack_token):
        threading.Thread.__init__(self)
        self.health_bot = health_bot
        self.slack_client = SlackClient(slack_token)
        self.running = False

    def run(self):
        self.running = True
        if self.slack_client.rtm_connect():
            print("Slackbot running.")
            while self.running:
                slack_output = self.slack_client.rtm_read()
                # if slack_output:
                #     print(slack_output)
                message, message_sender, channel = self.parse_slack_output(slack_output)
                if message:
                    print(message, message_sender, channel)
                if message and channel and channel[0] == 'D':
                    reply = self.health_bot.process_message(message_sender, message)
                    print(reply)
                    self.post_to_slack(reply['text'], channel)
                time.sleep(0.1)
        else:
            print("Connection failed. Invalid Slack token?")

    def stop(self):
        self.running = False

    def _is_user_text_message(self, output):
        return output and 'text' in output and 'user_profile' not in output and 'bot_id' not in output

    def _is_img_upload(self, output):
        return (output and output['type'] == 'message' and output.get('subtype') == 'file_share' and
                'file' in output and output['file'].get('mimetype', '').startswith('image/'))

    def parse_slack_output(self, slack_rtm_output):
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                if self._is_user_text_message(output):
                    return ({'type': 'text', 'content': output['text'].lower()},
                            output['user'], output['channel'])
                elif self._is_img_upload(output):
                    return ({'type': 'image', 'content': output['file']['url_private']},
                            output['user'], output['channel'])
        return None, None, None

    def post_to_slack(self, response, channel):
        self.slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
