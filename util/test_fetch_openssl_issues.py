#!/usr/bin/env python3
"""
Unit tests for fetch_openssl_issues.py

This test suite verifies the basic functionality of the fetch_openssl_issues script
without making actual API calls.
"""

import unittest
import sys
from unittest.mock import patch, MagicMock
from io import StringIO

# Import the script (this assumes the script is in the same directory)
import fetch_openssl_issues


class TestFetchOpenSSLIssues(unittest.TestCase):
    """Test cases for fetch_openssl_issues.py"""

    def test_print_issues_empty(self):
        """Test printing empty issues list"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            fetch_openssl_issues.print_issues([])
            output = fake_out.getvalue()
            self.assertIn("No issues found", output)

    def test_print_issues_with_data(self):
        """Test printing issues with data"""
        test_issues = [{
            'number': 12345,
            'title': 'Test Issue',
            'state': 'open',
            'created_at': '2023-01-01T00:00:00Z',
            'html_url': 'https://github.com/openssl/openssl/issues/12345',
            'comments': 5
        }]
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            fetch_openssl_issues.print_issues(test_issues)
            output = fake_out.getvalue()
            self.assertIn("Found 1 issue(s)", output)
            self.assertIn("#12345", output)
            self.assertIn("Test Issue", output)
            self.assertIn("open", output)

    def test_print_discussions_empty(self):
        """Test printing empty discussions list"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            fetch_openssl_issues.print_discussions([])
            output = fake_out.getvalue()
            self.assertIn("No discussions found", output)

    def test_print_discussions_with_data(self):
        """Test printing discussions with data"""
        test_discussions = [{
            'number': 100,
            'title': 'Test Discussion',
            'category': {'name': 'General'},
            'createdAt': '2023-01-01T00:00:00Z',
            'url': 'https://github.com/openssl/openssl/discussions/100',
            'comments': {'totalCount': 3},
            'answerChosenAt': None
        }]
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            fetch_openssl_issues.print_discussions(test_discussions)
            output = fake_out.getvalue()
            self.assertIn("Found 1 discussion(s)", output)
            self.assertIn("#100", output)
            self.assertIn("Test Discussion", output)
            self.assertIn("General", output)

    @patch('fetch_openssl_issues.urlopen')
    def test_fetch_github_api_success(self, mock_urlopen):
        """Test successful GitHub API fetch"""
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"test": "data"}'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response
        
        result = fetch_openssl_issues.fetch_github_api('https://api.github.com/test')
        self.assertEqual(result, {"test": "data"})

    @patch('fetch_openssl_issues.urlopen')
    @patch('sys.exit')
    def test_fetch_github_api_http_error(self, mock_exit, mock_urlopen):
        """Test GitHub API fetch with HTTP error"""
        from urllib.error import HTTPError
        
        mock_urlopen.side_effect = HTTPError(
            'https://api.github.com/test',
            403,
            'Forbidden',
            {},
            None
        )
        
        with patch('sys.stderr', new=StringIO()):
            fetch_openssl_issues.fetch_github_api('https://api.github.com/test')
            mock_exit.assert_called_once_with(1)

    def test_command_line_help(self):
        """Test command line help output"""
        with patch('sys.argv', ['fetch_openssl_issues.py', '--help']):
            with self.assertRaises(SystemExit) as cm:
                fetch_openssl_issues.main()
            # Help should exit with 0
            self.assertEqual(cm.exception.code, 0)

    @patch('sys.argv', ['fetch_openssl_issues.py'])
    def test_command_line_missing_username(self):
        """Test command line with missing required username"""
        with self.assertRaises(SystemExit) as cm:
            fetch_openssl_issues.main()
        # Should exit with error code 2 (argparse error)
        self.assertEqual(cm.exception.code, 2)


class TestIssueFiltering(unittest.TestCase):
    """Test cases for issue filtering logic"""

    def test_filter_pull_requests(self):
        """Test that pull requests are filtered from issues"""
        test_data = [
            {'number': 1, 'title': 'Issue 1'},
            {'number': 2, 'title': 'PR 1', 'pull_request': {}},
            {'number': 3, 'title': 'Issue 2'},
        ]
        
        # Simulate the filtering logic used in fetch_issues
        filtered = [item for item in test_data if 'pull_request' not in item]
        
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0]['number'], 1)
        self.assertEqual(filtered[1]['number'], 3)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
