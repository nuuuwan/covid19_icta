"""Uploaded data to nuuuwan/covid19_icta:data branch."""

import os


def upload_data():
    """Upload data."""
    os.system('echo "test data" > /tmp/covid19_icta.test.txt')
    os.system('echo "# covid19_icta" > /tmp/README.md')


if __name__ == '__main__':
    upload_data()
