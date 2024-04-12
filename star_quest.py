import argparse
import requests
import os
import sys
from rich import print
from typing import List, Dict, Any
from typing import List, Dict, Any, Optional

banner = """
             .                                                                         .   
           .o8                                                                       .o8   
 .oooo.o .o888oo  .oooo.   oooo d8b       .ooooo oo oooo  oooo   .ooooo.   .oooo.o .o888oo 
d88(  "8   888   `P  )88b  `888""8P      d88' `888  `888  `888  d88' `88b d88(  "8   888   
`"Y88b.    888    .oP"888   888          888   888   888   888  888ooo888 `"Y88b.    888   
o.  )88b   888 . d8(  888   888          888   888   888   888  888    .o o.  )88b   888 . 
8""888P'   "888" `Y888""8o d888b         `V8bod888   `V88V"V8P' `Y8bod8P' 8""888P'   "888" 
                                               888.                                        
                                               8P'                                         
                                               "                                           
"""

def get_user_or_org_type(username: str) -> Optional[str]:
    """Determines if the username corresponds to a user or an organization, taking into account the GitHub API rate limit."""
    url = f'https://api.github.com/users/{username}'
    response = requests.get(url)
    user_data: Dict[str, Any] = response.json()
    
    # Check for rate limit exceeded message
    if 'message' in user_data and 'API rate limit exceeded' in user_data['message']:
        # Handle rate limit exceeded (e.g., by returning a special value or raising an exception)
        print("[bold red]API rate limit exceeded. Please try again later or authenticate to increase your rate limit.[/bold red]")
        return None
    
    if 'type' in user_data:
        return user_data['type']  # Can be 'User' or 'Organization'
    
    return None

def get_all_repos(username: str, is_org: bool = False) -> List[Dict[str, Any]]:
    """Fetches all repositories for a given user or organization, sorted by star count."""
    repos: List[Dict[str, Any]] = []
    page: int = 1
    base_url: str = "https://api.github.com/orgs/" if is_org else "https://api.github.com/users/"
    url: str = f"{base_url}{username}/repos"

    while True:
        response = requests.get(f"{url}?page={page}&per_page=100")
        page_data: List[Dict[str, Any]] = response.json()

        if response.status_code != 200 or not page_data:
            break

        repos.extend(page_data)
        page += 1

    if isinstance(repos, list):
        return sorted(repos, key=lambda x: x['stargazers_count'], reverse=True)
    else:
        print(f"{username} not found or error fetching repos.")
        return []
    

def print_repos_stars(username: str, repos: List[Dict[str, Any]], verbose: bool = False) -> None:
    """Prints sorted repositories by stars for a user or organization."""
    total_stars: int = 0
    total_repos: int = len(repos)
    print(f'\nGitHub user: [bold green]{username}[/bold green]\n')
    for repo in repos:
        if not verbose:
            if repo['stargazers_count'] == 0:
                break
        print(f"{repo['name'].ljust(30)}: {repo['stargazers_count']} stars")
        total_stars += repo['stargazers_count']
    print(f"\n[bold white]Total repositories for {username}:[/bold white] {total_repos}")
    print(f"[bold white]Total stars for {username}:[/bold white] {total_stars}")

def process_username(username: str, verbose: bool = False) -> None:
    """Processes a GitHub username or organization, fetching repositories and contributors if applicable."""
    user_type: str = get_user_or_org_type(username)
    if user_type is None:
        print(f"{username} does not exist")
        return
    
    is_org: bool = user_type == 'Organization'
    repos: List[Dict[str, Any]] = get_all_repos(username, is_org)
    print_repos_stars(username, repos, verbose)
    
    # For organizations, additionally print contributors for each repo
    if is_org:
        for repo in repos:
            print(f"\nContributors for {repo['name']}:")
            contributors_url: str = repo['contributors_url']
            contributors: List[Dict[str, Any]] = requests.get(contributors_url).json()
            for contributor in contributors:
                if isinstance(contributor, dict):
                    print(f"{contributor['login'].ljust(30)}: {contributor.get('contributions', 'N/A')} contributions")
            print("\n")

def process_file(file_path: str, verbose: bool = False) -> None:
    """Processes each username in the given file."""
    try:
        with open(file_path, 'r') as file:
            for line in file:
                username = line.strip()
                if username:
                    process_username(username, verbose)
    except FileNotFoundError:
        print(f"File {file_path} not found.")

def is_file(path):
    """Check if a path is an existing file."""
    return os.path.isfile(path)

# Initialize parser
parser = argparse.ArgumentParser(description='Process GitHub usernames or files containing usernames and tell you how many stars they have.')
parser.add_argument('username', nargs='+', help='GitHub Usernames or Orginization. Or files with usernames')
parser.add_argument('-v','--verbose', action='store_true', help='Show all repositories, even those with 0 stars')

if len(sys.argv)==1:
    print(f"{banner}")
    parser.print_help()
    sys.exit(1)

# Parse arguments
args = parser.parse_args()

for arg in args.username:
    if is_file(arg):
        process_file(arg, args.verbose)
    else:
        process_username(arg, args.verbose)
