import argparse
import datetime
import json
import requests
import sys


def get_top_urls_with_issues(repositories_json):
    return [
            (repo['html_url'], repo['open_issues_count'])
            for repo in repositories_json
            ]


def output_urls_with_issues_to_console(urls_with_issues, rep_count, days):
    print('\n Top {} github repositories created for the last {} days:\n'
          .format(rep_count, days))
    print('№   {:<70} | {:<10}'.format('URL', 'Open issues'))
    for count, (url, issue) in enumerate(urls_with_issues, 1):
        print('{:<3} {:<70} | {:<10}'.format(count, url, issue))
    print()


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--days', default=7, type=int,
                        help='number of the days')
    parser.add_argument('-c', '--count', default=30, type=int,
                        help='quantity of the top repositories')
    return parser


def request_new_github_repos_api(days, rep_count):
    github_repositories = 'https://api.github.com/search/repositories'
    payload = {
              'q': {'created': stringify_passed_days(days=days),
                    'sort': 'stars',
                    'order': 'desc'},
              'per_page': rep_count,
              }
    response = requests.get(github_repositories, params=payload)
    if not response.ok:
        response.raise_for_status()
    return json.loads(response.text)['items']


def stringify_passed_days(days):
    passed_days = datetime.datetime.now() - datetime.timedelta(days=days)
    return '>{:%Y-%m-%d}'.format(passed_days)


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    days, rep_count = namespace.days, namespace.count
    new_github_repos_json = request_new_github_repos_api(days, rep_count)
    top_urls_with_issues = get_top_urls_with_issues(new_github_repos_json)
    output_urls_with_issues_to_console(top_urls_with_issues, rep_count, days)
