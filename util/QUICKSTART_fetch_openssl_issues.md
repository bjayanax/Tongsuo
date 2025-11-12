# Quick Start Guide: Fetch OpenSSL Issues

This guide will help you quickly start using the fetch_openssl_issues script to find issues or discussions you've created in the OpenSSL repository.

## Quick Examples

### 1. Find all your issues (most common use case)

```bash
python3 util/fetch_openssl_issues.py -u YOUR_GITHUB_USERNAME
```

Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username.

### 2. Find only open issues

```bash
python3 util/fetch_openssl_issues.py -u YOUR_GITHUB_USERNAME -s open
```

### 3. Find issues and save to a file

```bash
python3 util/fetch_openssl_issues.py -u YOUR_GITHUB_USERNAME --json > my_issues.json
```

### 4. Use with GitHub token (recommended)

If you're hitting rate limits or want to fetch discussions:

```bash
export GITHUB_TOKEN="your_token_here"
python3 util/fetch_openssl_issues.py -u YOUR_GITHUB_USERNAME -t $GITHUB_TOKEN
```

### 5. Fetch both issues and discussions

```bash
python3 util/fetch_openssl_issues.py -u YOUR_GITHUB_USERNAME -d -t $GITHUB_TOKEN
```

## Using the Bash Wrapper

For convenience, you can also use the bash wrapper:

```bash
./util/fetch-openssl-issues.sh -u YOUR_GITHUB_USERNAME
```

## Common Issues

### "Rate limit exceeded"

**Problem**: You see "HTTP Error: 403 - Forbidden" with rate limit message.

**Solution**: Get a GitHub token and use it with `-t TOKEN`:
1. Go to https://github.com/settings/tokens
2. Generate a new token (classic)
3. Select `public_repo` scope
4. Copy the token
5. Use: `python3 util/fetch_openssl_issues.py -u USERNAME -t YOUR_TOKEN`

### Cannot fetch discussions

**Problem**: Discussions are not being returned.

**Solution**: Discussions require a GitHub token:
```bash
python3 util/fetch_openssl_issues.py -u USERNAME -d -t YOUR_TOKEN
```

## Output Format

### Standard Output
```
================================================================================
Found 3 issue(s)
================================================================================

#12345: Fix memory leak in SSL_connect
  State: open
  Created: 2023-01-15T10:30:00Z
  URL: https://github.com/openssl/openssl/issues/12345
  Comments: 5

#12346: Documentation update for EVP_PKEY
  State: closed
  Created: 2023-02-20T14:15:00Z
  URL: https://github.com/openssl/openssl/issues/12346
  Comments: 2
```

### JSON Output
```json
{
  "username": "your_username",
  "issues": [
    {
      "number": 12345,
      "title": "Fix memory leak in SSL_connect",
      "state": "open",
      "created_at": "2023-01-15T10:30:00Z",
      "html_url": "https://github.com/openssl/openssl/issues/12345",
      "comments": 5
    }
  ],
  "discussions": []
}
```

## Advanced Usage

### Piping to grep
Find issues containing specific keywords:
```bash
python3 util/fetch_openssl_issues.py -u USERNAME | grep -i "ssl"
```

### Counting issues
```bash
python3 util/fetch_openssl_issues.py -u USERNAME --json | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'Total: {len(data[\"issues\"])}')"
```

### Filter by date using jq
```bash
python3 util/fetch_openssl_issues.py -u USERNAME --json | jq '.issues[] | select(.created_at >= "2023-01-01")'
```

## Need More Help?

- See the full documentation: `util/README_fetch_openssl_issues.md`
- Run: `python3 util/fetch_openssl_issues.py --help`
- Check the test file for examples: `util/test_fetch_openssl_issues.py`

## Script Location

The scripts are located in the `util/` directory:
- Main script: `util/fetch_openssl_issues.py`
- Bash wrapper: `util/fetch-openssl-issues.sh`
- Documentation: `util/README_fetch_openssl_issues.md`
- Tests: `util/test_fetch_openssl_issues.py`
