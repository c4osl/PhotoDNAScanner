#!/usr/bin/env python3
import os
import sys
import argparse
from scanner import FileScanner
from config import Config
from api_client import PhotoDNAClient

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Scan files using Microsoft Content Moderator API'
    )
    parser.add_argument(
        'path',
        help='File or directory to scan'
    )
    parser.add_argument(
        '--config',
        default='~/.photodna/config.ini',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--recursive',
        '-r',
        action='store_true',
        help='Scan directories recursively'
    )
    return parser.parse_args()

def main():
    args = parse_arguments()

    try:
        config = Config(os.path.expanduser(args.config))
        api_client = PhotoDNAClient(config.get_api_key())
        scanner = FileScanner(api_client)

        path = os.path.abspath(args.path)
        if not os.path.exists(path):
            print(f"Error: Path does not exist: {path}")
            sys.exit(1)

        results = scanner.scan(path, recursive=args.recursive)

        # Print results
        print("\nScan Results:")
        print("-" * 80)

        for result in results:
            status = "MATCH" if result['match'] else "CLEAN"
            print(f"{status}: {result['file']}")
            if result['match'] and result.get('details'):
                print(f"Details: {result['details']}")
            print("-" * 80)

        if any(r['match'] for r in results):
            sys.exit(1)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()