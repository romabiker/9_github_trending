import datetime
import json
import requests
import sys


def stringify_last_weeks(weeks=1):
    last_week = datetime.datetime.now() - datetime.timedelta(weeks=weeks)
    return '>{:%Y-%m-%d}'.format(last_week)


def request_new_github_repos_api(weeks=1):
    github_repositories = 'https://api.github.com/search/repositories'
    payload = {
                'q': {'created': stringify_last_weeks(weeks=weeks),
                      'sort': 'stars',
                      'order': 'desc'}
              }
    response = requests.get(github_repositories, params=payload)
    if not response.ok:
        response.raise_for_status()
    return json.loads(response.text)


def get_top_urls_with_issues(repositories_json):
    return [
            (repo['html_url'], repo['open_issues_count'])
            for repo in repositories_json['items'][:20]
            ]


def output_urls_with_issues_to_console(urls_with_issues):
    print('\n Top 20 github repositories created for the last week:\n')
    print('№   {:<70} | {:<10}'.format('URL', 'Open issues'))
    for count, (url, issue) in enumerate(urls_with_issues, 1):
        print('{:<3} {:<70} | {:<10}'.format(count, url, issue))
    print()


if __name__ == '__main__':
    new_github_repos_json = request_new_github_repos_api()
    top_urls_with_issues = get_top_urls_with_issues(new_github_repos_json)
    output_urls_with_issues_to_console(top_urls_with_issues)
