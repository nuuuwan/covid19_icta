"""Uploaded data to nuuuwan/covid19_icta:data branch."""


from covid19_icta import scrape, tweet


def upload_data():
    html, image_file, table_image_file = scrape.scrape()
    center_list = scrape.parse_center_list(html)
    tweet.tweet_status(
        center_list,
        image_file,
        table_image_file,
    )


if __name__ == '__main__':
    upload_data()
