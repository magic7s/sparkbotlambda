"""A sample AWS Lambda function that can be used with a Cisco Spark Bot
for fetching information triggered by Spark messages.

A Spark Webhook can be created to trigger an HTTP POST to a targetUrl
such as an AWS API Gateway endpoint.

In this example, the Spark message id is extracted from the Webhook triggered POST to AWS (lambda_handler)
 """

from __future__ import print_function

import json
import requests
import os

spark_header = {
    'content-type': "application/json; charset=utf-8",
    'authorization': os.environ['SPARKAPITOKEN'],
    'cache-control': "no-cache"
}
spark_url = 'https://api.ciscospark.com/v1/messages'


def get_spark_selfId():
	spark_people_url = 'https://api.ciscospark.com/v1/people/me'
	get_text = requests.get(spark_people_url, headers=spark_header)
	t = json.loads(get_text.text)
	return t['id']

# the lambda handler function
def lambda_handler(event, context):
    """Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.
    """
    # print the event details received from the Spark Webhook for logging
    print("Received event: " + json.dumps(event, indent=2))
    #check if self generated this event
    if event['actorId'] == get_spark_selfId():
    	print("Ignoring event due to actorId = me")
    	return 0
    # assign the Spark message id to a variable
    msg_id = event['data']['id']
    # assign the Spark roomId to a variable (for the Bot to respond into the right room dynamically)
    room_id = event['data']['roomId']
    spark_msg_url = '{0}/{1}'.format(str(spark_url), str(msg_id))
    print("Requesting URL: " + str(spark_msg_url))
    get_text = requests.get(spark_msg_url, headers=spark_header)
    if not get_text.status_code == 200:
    	print("Error Received Code: " + str(get_text.status_code))
    	return 0
    t = json.loads(get_text.text)
    if t['text']:
        response = 'TEST MESSAGE RECEIVED: ' + t['text']
        payload = {'roomId': str(room_id),
                   'text': str(response)
                   }
        spark_response = requests.post(spark_url, data=json.dumps(payload), headers=spark_header)
        print(spark_response.status_code)

    else:
        print("Error: No Text Received in msg")

    return "Finished"
