import logging
import tweepy

from twitter_auth import TwitterAuthenticator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class TweetListener(tweepy.StreamListener):
    BOT_HANDLE = 'ReclusiveCoder'
    IGNORE_TERMS = ["SSR", "Sushant"]
    TERMS_MAP = {"committed suicide": "died by suicide", "commits suicide": "dies by suicide",
                 "committing suicide": "dying by suicide", "commit suicide": "die by suicide"}
    correctionCount = 0

    def __init__(self, the_api):
        super().__init__()
        self.api = the_api
        self.me = the_api.me()

    def on_status(self, tweet):
        logger.info(f"@{tweet.user.screen_name}:-->    {tweet.text}")

        # exclude bot handle later
        if TweetListener.BOT_HANDLE == tweet.user.screen_name and \
                not any(ignore_term in tweet.text.lower() for ignore_term in TweetListener.IGNORE_TERMS) and \
                not any(app_term in tweet.text.lower() for app_term in TweetListener.TERMS_MAP.values()):

            for inapp_term in TweetListener.TERMS_MAP.keys():
                if inapp_term in tweet.text.lower():
                    original_txt, corrected_txt = self._get_contextual_texts(inapp_term, tweet.text.lower())
                    self.api.update_status(f"It is more sensitive to write this as '{corrected_txt}' "
                                           f"instead of accusatory '{original_txt}'.\n\n"
                                           "Would you please consider rephrasing it appropriately?",
                                           in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
                    TweetListener.correctionCount += 1
                    logger.info(f"@@@@@@---------->>> Corrected suicide tweet # {TweetListener.correctionCount}")

    def on_error(self, status):
        logger.error(f"Error detected: {status}")

    def _get_contextual_texts(self, key_phrase, tweet_text):
        sui_idx = tweet_text.find(key_phrase)
        lword_idx = tweet_text.rfind(" ", 0, sui_idx - 1) if tweet_text.rfind(" ", 0, sui_idx - 1) > 0 else 0
        rword_idx = tweet_text.find(" ", sui_idx + len(key_phrase) + 1)
        extracted_text = tweet_text[lword_idx:rword_idx].strip()

        return extracted_text, extracted_text.replace(key_phrase, TweetListener.TERMS_MAP[key_phrase])


# Authenticate & Run
def main():
    api = TwitterAuthenticator.get_authenticated_api()
    tweets_listener = TweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=TweetListener.TERMS_MAP.keys(), languages=["en"])


if __name__ == "__main__":
    main()
