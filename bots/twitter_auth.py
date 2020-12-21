import tweepy
import logging
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

logger = logging.getLogger()

class TwitterAuthenticator:

    @staticmethod
    def get_authenticated_api():
        _apiKey = os.getenv("API_KEY")
        _apiSec = os.getenv("API_SEC")
        _accessToken = os.getenv("ACCESS_TOKEN")
        _accessSec = os.getenv("ACCESS_SEC")

        auth = tweepy.OAuthHandler(_apiKey, _apiSec)
        auth.set_access_token(_accessToken, _accessSec)

        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        # validate credential
        try:
            api.verify_credentials()
            logger.info("Twitter Auth successful")
        except Exception as e:
            logger.error("Error during Twitter Auth", exc_info=True)
            raise e

        return api

