import pymsteams #pip install pymsteams

def postea_slack(texto_postear):
    # Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
    webhook_url = 'https://hooks.slack.com/services/TB570HPBL/BB5S4R1TN/'
    slack_data = {'text': texto_postear}
    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )

def postea_Teams(texto_postear):
    # You must create the connectorcard object with the Microsoft Webhook URL
    myTeamsMessage = pymsteams.connectorcard("https://011h.webhook.office.com/webhookb2/fe9b10ad-c072-4a8a-9eaa-ef39d4bee785")
    # Add text to the message.
    myTeamsMessage.text(texto_postear)
    # send the message.
    myTeamsMessage.send()