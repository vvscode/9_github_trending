from datetime import date, timedelta
import requests


def get_trending_repositories(top_size, period_size=1):
    date_from = date.today() - timedelta(days=period_size)
    repositories = requests.get('https://api.github.com/search/repositories', {
        'q': 'created:>{}'.format(date_from.isoformat()),
        'sort': 'stars',
        'order': 'desc',
        'per_page': top_size
    }).json()['items']
    return repositories


def get_open_issues_amount(repo_owner, repo_name):
    response = requests.get('https://api.github.com/repos/{}/{}/issues'.format(
        repo_owner,
        repo_name
    )).json()
    return len(response)


if __name__ == '__main__':
    top_size = 20
    week_days = 7
    try:
        for repo in get_trending_repositories(top_size, period_size=week_days):
            repo_owner_name = repo['owner']['login']
            repo_name = repo['name']
            issues_count = get_open_issues_amount(repo_owner_name, repo_name)
            print('URL: {}\tStars: {}\tIssues: {}'.format(
                repo['html_url'],
                repo['stargazers_count'],
                issues_count
            ))
    except requests.exceptions.RequestException as e:
        print('Script requires internet connection')
        print('Please check if everything is fine and restart')
