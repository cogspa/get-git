import requests
import csv

def fetch_latest_commit_date(username, repo_name):
    url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
    response = requests.get(url, params={'per_page': 1})  # Fetch only the latest commit

    if response.status_code != 200:
        print(f"Error fetching commits for {repo_name}. Status code: {response.status_code}")
        return None

    commits = response.json()
    if commits:
        return commits[0]['commit']['committer']['date']
    return None

def fetch_github_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error fetching data for {username}. Status code: {response.status_code}")
        return []

    repos = response.json()
    for repo in repos:
        repo['latest_commit_date'] = fetch_latest_commit_date(username, repo['name'])

    # Sort the repositories by creation date in descending order
    repos.sort(key=lambda x: x['created_at'], reverse=True)

    return repos



def save_to_csv(repos, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Repository Name', 'Repository Link', 'Creation Date', 'Latest Contribution Date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for repo in repos:
            writer.writerow({
                'Repository Name': repo['name'],
                'Repository Link': repo['html_url'],
                'Creation Date': repo['created_at'],
                'Latest Contribution Date': repo.get('latest_commit_date', 'N/A')
            })


if __name__ == "__main__":
    username = input("Enter your GitHub username: ")
    repos = fetch_github_repos(username)
    
    if repos:
        save_to_csv(repos, f"{username}_repos.csv")
        print(f"Data saved to {username}_repos.csv")
    else:
        print("No data to save.")

