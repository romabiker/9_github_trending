import datetime
import json
import requests
import sys


def get_top_urls_with_issues(repositories_json):
    return [
            (repo['html_url'], repo['open_issues_count'])
            for repo in repositories_json
            ]


def output_urls_with_issues_to_console(urls_with_issues):
    print('\n Top {} github repositories created for the last {} days:\n'
          .format(days, repos_quantity))
    print('№   {:<70} | {:<10}'.format('URL', 'Open issues'))
    for count, (url, issue) in enumerate(urls_with_issues, 1):
        print('{:<3} {:<70} | {:<10}'.format(count, url, issue))
    print()


def prompt_days_repos_quantity():
    try:
        return (
                int(input('Enter days:  ')),
                int(input('Enter quantity:  '))
                )
    except ValueError as e:
        print('You have enter digits')
        print('Example: Enter days:  7')
        print('Example: Enter quantity:  20')
        sys.exit()


def request_new_github_repos_api(days, quantity):
    github_repositories = 'https://api.github.com/search/repositories'
    payload = {
                'q': {'created': stringify_passed_days(days=days),
                      'sort': 'stars',
                      'order': 'desc'}
              }
    response = requests.get(github_repositories, params=payload)
    if not response.ok:
        response.raise_for_status()
    return json.loads(response.text)['items'][:quantity]


def stringify_passed_days(days):
    passed_days = datetime.datetime.now() - datetime.timedelta(days=days)
    return '>{:%Y-%m-%d}'.format(passed_days)


if __name__ == '__main__':
    days, repos_quantity = prompt_days_repos_quantity()
    new_github_repos_json = request_new_github_repos_api(days, repos_quantity)
    top_urls_with_issues = get_top_urls_with_issues(new_github_repos_json)
    output_urls_with_issues_to_console(top_urls_with_issues)
