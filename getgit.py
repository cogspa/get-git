import requests
import csv

def fetch_github_repos(username):
    url = f"https://api.github.com/users/{cogspa}/repos"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error fetching data for {cogspa}. Status code: {response.status_code}")
        return []

    return response.json()

def save_to_csv(repos, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Repository Name', 'Repository Link', 'Creation Date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for repo in repos:
            writer.writerow({'Repository Name': repo['name'], 'Repository Link': repo['html_url'], 'Creation Date': repo['created_at']})

if __name__ == "__main__":
    username = input("Enter your GitHub username: ")
    repos = fetch_github_repos(username)
    
    if repos:
        save_to_csv(repos, f"{username}_repos.csv")
        print(f"Data saved to {username}_repos.csv")
    else:
        print("No data to save.")

