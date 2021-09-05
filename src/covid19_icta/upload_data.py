"""Uploaded data to nuuuwan/covid19_icta:data branch."""


from covid19_icta import scrape


def upload_data():
    html, image_file, table_image_file = scrape.scrape()
    message, center_list = scrape.parse_and_tweet(html)
    tweet.tweet_status(
        message,
        center_list,
        image_file,
        table_image_file,
    )


if __name__ == '__main__':
    upload_data()
