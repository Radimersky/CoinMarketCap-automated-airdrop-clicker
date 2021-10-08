from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets


# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


# This code sample shows how to add a channel subscription.
# The default channel-id is for the GoogleDevelopers YouTube channel.
# Sample usage:
# python add_subscription.py --channel-id=UC_x5XG1OV2P6uZZ5FSM9Ttw

# import google.oauth2.credentials
# import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# https://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html

# CLIENT_SECRETS_FILE = 'client_secret.json'
def get_authenticated_service(CLIENT_SECRETS_FILE):
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)

  cred = flow.run_local_server(
      host='localhost',
      port=8088,
      authorization_prompt_message='Please visit this URL: {url}',
      success_message='The auth flow is complete; you may close this window.',
      open_browser=True)

  with open('refresh.token', 'w+') as f:
      f.write(cred._refresh_token)

  print('Refresh Token:', cred._refresh_token)
  print('Saved Refresh Token to file: refresh.token')

  return build(API_SERVICE_NAME, API_VERSION, credentials = cred)



# def get_authenticated_service():
#   flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
#   credentials = flow.run_console()

#   return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)



# This method calls the API's youtube.subscriptions.insert method to add a
# subscription to the specified channel.
def add_subscription(youtube, channel_id):
  try:
    add_subscription_response = youtube.subscriptions().insert(
      part='snippet',
      body=dict(
        snippet=dict(
          resourceId=dict(
            channelId=channel_id
          )
        )
      )).execute()

  except HttpError as e:
    print('Error in Youtube channel with id %s with error code %d and reason:\n%s' % (channel_id, e.resp.status, e.reason))
    if(e.resp.status is 404):
      return False
  else:
      print('A subscription to \'%s\' was added.' % channel_id)
  return True



## HOW TO USE ##

# import argparse
# import os
# import re
# from googleapiclient.errors import HttpError

# youtube = get_authenticated_service()
# channel_id = "UC3L64zz-sbwaEgMVotqLkTA"
# add_subscription(youtube, channel_id)
# try:
#     channel_title = add_subscription(youtube, channel_id)
# except HttpError as e:
#     print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
# else:
#     print('A subscription to \'%s\' was added.' % channel_title)