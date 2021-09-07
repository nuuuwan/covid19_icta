"""Tweet."""

from utils import timex, twitter

MAX_TWEET_LEN = 250


def tweet_status(
    center_list,
    image_file,
    table_image_file,
):

    date_to_center_list = {}
    for center in center_list:
        date = center['date']
        if date not in date_to_center_list:
            date_to_center_list[date] = []
        date_to_center_list[date].append(center)

    inner_lines = []
    for date, date_center_list in date_to_center_list.items():
        inner_lines.append(
            '{date}: {n_centers} centers '.format(
                date=date,
                n_centers=len(date_center_list),
            )
        )
    inner = '\n'.join(inner_lines)

    time_str = timex.format_time(timex.get_unixtime(), '%I:%M%p, %Y-%m-%d')

    tweet_text = '''Citizen Registration Portal - @icta_srilanka
Status as of {time_str}

"{message}"

{inner}

Details & Register at https://vaccine.covid19.gov.lk/sign-in
#COVID19SL #SriLanka #lka
    '''.format(
        time_str=time_str,
        message=message,
        inner=inner,
    )

    image_files = [image_file]
    if table_image_file:
        image_files.append(table_image_file)
    twtr = twitter.Twitter.from_args()
    twtr.tweet(
        tweet_text=tweet_text,
        status_image_files=image_files,
        update_user_profile=True,
    )
