#!/usr/bin/env python3
"""
Script to fetch OpenSSL issues or discussion tickets raised by a specific user.

This script uses the GitHub API to retrieve issues and discussions from the
openssl/openssl repository that were created by a specified user.
"""

import sys
import json
import argparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def fetch_github_api(url, token=None):
    """
    Fetch data from GitHub API.
    
    Args:
        url: The API endpoint URL
        token: Optional GitHub personal access token for higher rate limits
        
    Returns:
        Parsed JSON response
    """
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'Tongsuo-Fetch-Issues'
    }
    
    if token:
        headers['Authorization'] = f'token {token}'
    
    try:
        request = Request(url, headers=headers)
        with urlopen(request) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}", file=sys.stderr)
        if e.code == 403:
            print("Rate limit may be exceeded. Consider using a GitHub token with -t option.", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"URL Error: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def fetch_issues(username, state='all', token=None):
    """
    Fetch issues from openssl/openssl repository created by the specified user.
    
    Args:
        username: GitHub username
        state: Issue state filter ('open', 'closed', or 'all')
        token: Optional GitHub token
        
    Returns:
        List of issues
    """
    base_url = "https://api.github.com/repos/openssl/openssl/issues"
    params = f"?creator={username}&state={state}&per_page=100"
    url = base_url + params
    
    issues = []
    page = 1
    
    while True:
        page_url = f"{url}&page={page}"
        response = fetch_github_api(page_url, token)
        
        if not response:
            break
            
        # Filter out pull requests (GitHub API returns both issues and PRs in /issues endpoint)
        page_issues = [item for item in response if 'pull_request' not in item]
        issues.extend(page_issues)
        
        if len(response) < 100:
            break
        page += 1
    
    return issues


def fetch_discussions(username, token=None):
    """
    Fetch discussions from openssl/openssl repository created by the specified user.
    
    Note: This requires GitHub GraphQL API and a token.
    
    Args:
        username: GitHub username
        token: GitHub token (required for GraphQL API)
        
    Returns:
        List of discussions
    """
    if not token:
        print("Warning: GitHub token is required to fetch discussions via GraphQL API", file=sys.stderr)
        return []
    
    query = """
    query($cursor: String) {
      repository(owner: "openssl", name: "openssl") {
        discussions(first: 100, after: $cursor) {
          pageInfo {
            hasNextPage
            endCursor
          }
          nodes {
            title
            url
            number
            createdAt
            author {
              login
            }
            category {
              name
            }
            answerChosenAt
            comments(first: 1) {
              totalCount
            }
          }
        }
      }
    }
    """
    
    url = "https://api.github.com/graphql"
    discussions = []
    cursor = None
    
    while True:
        variables = {"cursor": cursor}
        payload = json.dumps({"query": query, "variables": variables}).encode()
        
        headers = {
            'Authorization': f'bearer {token}',
            'Content-Type': 'application/json',
            'User-Agent': 'Tongsuo-Fetch-Issues'
        }
        
        try:
            request = Request(url, data=payload, headers=headers)
            with urlopen(request) as response:
                result = json.loads(response.read().decode())
                
                if 'errors' in result:
                    print(f"GraphQL Error: {result['errors']}", file=sys.stderr)
                    break
                
                nodes = result['data']['repository']['discussions']['nodes']
                
                # Filter discussions by author
                user_discussions = [d for d in nodes if d['author'] and d['author']['login'] == username]
                discussions.extend(user_discussions)
                
                page_info = result['data']['repository']['discussions']['pageInfo']
                if not page_info['hasNextPage']:
                    break
                cursor = page_info['endCursor']
                
        except Exception as e:
            print(f"Error fetching discussions: {e}", file=sys.stderr)
            break
    
    return discussions


def print_issues(issues):
    """Print issues in a formatted manner."""
    if not issues:
        print("No issues found.")
        return
    
    print(f"\n{'='*80}")
    print(f"Found {len(issues)} issue(s)")
    print(f"{'='*80}\n")
    
    for issue in issues:
        print(f"#{issue['number']}: {issue['title']}")
        print(f"  State: {issue['state']}")
        print(f"  Created: {issue['created_at']}")
        print(f"  URL: {issue['html_url']}")
        print(f"  Comments: {issue['comments']}")
        print()


def print_discussions(discussions):
    """Print discussions in a formatted manner."""
    if not discussions:
        print("No discussions found.")
        return
    
    print(f"\n{'='*80}")
    print(f"Found {len(discussions)} discussion(s)")
    print(f"{'='*80}\n")
    
    for discussion in discussions:
        print(f"#{discussion['number']}: {discussion['title']}")
        print(f"  Category: {discussion['category']['name']}")
        print(f"  Created: {discussion['createdAt']}")
        print(f"  URL: {discussion['url']}")
        print(f"  Comments: {discussion['comments']['totalCount']}")
        answered = "Yes" if discussion['answerChosenAt'] else "No"
        print(f"  Answered: {answered}")
        print()


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Fetch OpenSSL issues or discussion tickets raised by a specific user',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -u username              # Fetch all issues
  %(prog)s -u username -s open      # Fetch only open issues
  %(prog)s -u username -d           # Fetch discussions (requires token)
  %(prog)s -u username -d -t TOKEN  # Fetch issues and discussions with token
        """
    )
    
    parser.add_argument('-u', '--username', required=True,
                        help='GitHub username to search for')
    parser.add_argument('-s', '--state', default='all',
                        choices=['open', 'closed', 'all'],
                        help='Filter issues by state (default: all)')
    parser.add_argument('-d', '--discussions', action='store_true',
                        help='Fetch discussions (requires GitHub token)')
    parser.add_argument('-t', '--token',
                        help='GitHub personal access token for higher rate limits and discussions')
    parser.add_argument('--json', action='store_true',
                        help='Output results in JSON format')
    
    args = parser.parse_args()
    
    # Fetch issues
    print(f"Fetching issues for user '{args.username}' from openssl/openssl repository...", file=sys.stderr)
    issues = fetch_issues(args.username, args.state, args.token)
    
    # Fetch discussions if requested
    discussions = []
    if args.discussions:
        print(f"Fetching discussions for user '{args.username}' from openssl/openssl repository...", file=sys.stderr)
        discussions = fetch_discussions(args.username, args.token)
    
    # Output results
    if args.json:
        result = {
            'username': args.username,
            'issues': issues,
            'discussions': discussions
        }
        print(json.dumps(result, indent=2))
    else:
        print_issues(issues)
        if args.discussions:
            print_discussions(discussions)


if __name__ == '__main__':
    main()
