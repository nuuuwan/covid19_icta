"""Tweet."""

from utils import timex, twitter

MAX_TWEET_LEN = 250


def tweet_status(
    message,
    center_list,
    image_file,
):

    date_to_center_list = {}
    for center in center_list:
        date = center['date']
        if date not in date_to_center_list:
            date_to_center_list[date] = []
        date_to_center_list[date].append(center)

    inner_lines = []
    for date, date_center_list in date_to_center_list.items():
        n_colombo = 0
        for center in date_center_list:
            if 'Colombo' in center['center']:
                n_colombo += 1

        has_colombo = 'incl. %d #Colombo' % (n_colombo) if n_colombo else ''
        inner_lines.append(
            '{date}: {n_centers} centers {has_colombo}'.format(
                date=date,
                n_centers=len(date_center_list),
                has_colombo=has_colombo,
            )
        )
    inner = '\n'.join(inner_lines)

    time_str = timex.format_time(timex.get_unixtime(), '%I:%M%p, %Y-%m-%d')

    tweet_text = '''Citizen Registration Portal (@icta_srilanka)
Status as of {time_str}

"{message}"

{inner}

More Details & Register at https://vaccine.covid19.gov.lk/sign-in
#COVID19SL #SriLanka #lka
    '''.format(
        time_str=time_str,
        message=message,
        inner=inner,
    )

    twtr = twitter.Twitter.from_args()
    twtr.tweet(
        tweet_text=tweet_text,
        status_image_files=[image_file],
        update_user_profile=True,
    )
