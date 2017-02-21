"""A sample AWS Lambda function that can be used with a Cisco Spark Bot
for fetching information triggered by Spark messages.

A Spark Webhook can be created to trigger an HTTP POST to a targetUrl
such as an AWS API Gateway endpoint.

In this example, the Spark message id is extracted from the Webhook triggered POST to AWS (lambda_handler)
 """

from __future__ import print_function

import json
import os
from ciscosparkapi import CiscoSparkAPI

api = CiscoSparkAPI(access_token=os.environ['SPARK_ACCESS_TOKEN'])

# the lambda handler function
def lambda_handler(event, context):
    """Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.
    """
    # print the event details received from the Spark Webhook for logging
    print("Received event: " + json.dumps(event, indent=2))
    #check if self generated this event
    if event['actorId'] == api.people.me().id:
    	print("Ignoring event due to actorId = me")
    	return 0
    # assign the Spark message id to a variable
    msg_id = event['data']['id']
    # assign the Spark roomId to a variable (for the Bot to respond into the right room dynamically)
    room_id = event['data']['roomId']
    
    t = api.messages.get(msg_id)
    if t.text:
        response = 'TEST MESSAGE RECEIVED: ' + t.text
        api.messages.create(roomId=room_id, text=response)
    else:
        print("Error: No Text Received in msg")

    return "Finished"
