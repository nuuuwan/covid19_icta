"""Uploaded data to nuuuwan/covid19_icta:data branch."""


from covid19_icta import scrape, tweet


def upload_data():
    html, image_file = scrape.scrape()
    message, center_list = scrape.parse_and_tweet(html, image_file)
    tweet.tweet_status(
        message,
        center_list,
        image_file,
    )


if __name__ == '__main__':
    upload_data()
