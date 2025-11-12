# Fetch OpenSSL Issues Script

## Overview

The `fetch_openssl_issues.py` script is a utility to fetch OpenSSL issues or discussion tickets raised by a specific GitHub user from the [openssl/openssl](https://github.com/openssl/openssl) repository.

## Features

- Fetch issues created by a specific user
- Filter issues by state (open, closed, or all)
- Fetch discussions created by a specific user (requires GitHub token)
- Support for GitHub personal access token to increase rate limits
- Output results in human-readable format or JSON

## Requirements

- Python 3.x
- Internet connection to access GitHub API

## Usage

### Basic Usage

Fetch all issues created by a user:

```bash
python3 util/fetch_openssl_issues.py -u <username>
```

### Filter by State

Fetch only open issues:

```bash
python3 util/fetch_openssl_issues.py -u <username> -s open
```

Fetch only closed issues:

```bash
python3 util/fetch_openssl_issues.py -u <username> -s closed
```

### Fetch Discussions

Fetch discussions (requires GitHub token):

```bash
python3 util/fetch_openssl_issues.py -u <username> -d -t <your_github_token>
```

### JSON Output

Output results in JSON format:

```bash
python3 util/fetch_openssl_issues.py -u <username> --json
```

### Combined Options

Fetch both issues and discussions with JSON output:

```bash
python3 util/fetch_openssl_issues.py -u <username> -d -t <your_github_token> --json
```

## GitHub Token

While the script can work without a GitHub token, using one is highly recommended to:

1. Avoid hitting GitHub API rate limits (60 requests/hour for unauthenticated vs 5000 requests/hour for authenticated)
2. Access discussions via the GraphQL API (required for discussions)

### Creating a GitHub Token

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token (classic)
3. Select appropriate scopes:
   - `public_repo` for reading public repository data
   - `read:discussion` for reading discussions
4. Copy the token and use it with the `-t` option

You can also set the token as an environment variable:

```bash
export GITHUB_TOKEN=<your_token>
python3 util/fetch_openssl_issues.py -u <username> -t $GITHUB_TOKEN
```

## Command-Line Options

| Option | Description |
|--------|-------------|
| `-u USERNAME`, `--username USERNAME` | GitHub username to search for (required) |
| `-s {open,closed,all}`, `--state {open,closed,all}` | Filter issues by state (default: all) |
| `-d`, `--discussions` | Fetch discussions (requires GitHub token) |
| `-t TOKEN`, `--token TOKEN` | GitHub personal access token |
| `--json` | Output results in JSON format |
| `-h`, `--help` | Show help message |

## Output Format

### Human-Readable Format

The default output format displays issues and discussions in a readable format:

```
================================================================================
Found 5 issue(s)
================================================================================

#12345: Issue Title
  State: open
  Created: 2023-01-15T10:30:00Z
  URL: https://github.com/openssl/openssl/issues/12345
  Comments: 3
```

### JSON Format

When using `--json`, the output is a JSON object containing:

```json
{
  "username": "example-user",
  "issues": [
    {
      "number": 12345,
      "title": "Issue Title",
      "state": "open",
      "created_at": "2023-01-15T10:30:00Z",
      "html_url": "https://github.com/openssl/openssl/issues/12345",
      "comments": 3
    }
  ],
  "discussions": []
}
```

## Examples

1. **Find all issues created by user "johndoe":**
   ```bash
   python3 util/fetch_openssl_issues.py -u johndoe
   ```

2. **Find only open issues:**
   ```bash
   python3 util/fetch_openssl_issues.py -u johndoe -s open
   ```

3. **Find issues and discussions with a token:**
   ```bash
   python3 util/fetch_openssl_issues.py -u johndoe -d -t ghp_xxxxxxxxxxxx
   ```

4. **Export results to a file in JSON format:**
   ```bash
   python3 util/fetch_openssl_issues.py -u johndoe --json > results.json
   ```

## Troubleshooting

### Rate Limit Exceeded

If you see "HTTP Error: 403 - Forbidden" with a message about rate limits:

- **Solution**: Use a GitHub personal access token with the `-t` option
- Without a token, you're limited to 60 requests per hour
- With a token, the limit increases to 5000 requests per hour

### Cannot Fetch Discussions

If discussions are not being fetched:

- **Solution**: Ensure you provide a GitHub token with the `-t` option
- Discussions require authentication via the GraphQL API

### No Issues Found

If the script reports no issues:

- Verify the username is correct
- Check if the user has actually created any issues in the openssl/openssl repository
- Try different state filters (open, closed, all)

## Notes

- The script only queries the [openssl/openssl](https://github.com/openssl/openssl) repository
- Pull requests are excluded from the issues results
- The script handles pagination automatically to fetch all matching results
- Both standard REST API (for issues) and GraphQL API (for discussions) are used

## License

This script is part of the Tongsuo project and follows the same license.
