#!/usr/bin/python
import argparse
import glob
import os

from github import Github
'''
upload_release.py - Uploads one or more files to a specified release for a Github repository

Author: Jordan Wright <jordan-wright>
'''


def main():
    parser = argparse.ArgumentParser(
        description='Upload assets to a given repository release')
    parser.add_argument('--repo', help='The repository to upload the asset to')
    parser.add_argument('--version', help='The version of the release')
    parser.add_argument(
        '--assets',
        help='The files to upload to the Github release',
        nargs='+')
    args = parser.parse_args()

    try:
        API_KEY = os.environ['GITHUB_API_KEY']
    except KeyError as e:
        print os.environ
        print('Error: Missing GITHUB_API_KEY  environment variable')
        return

    g = Github(API_KEY)

    # Verify the repo exists
    try:
        repo = g.get_repo(args.repo, lazy=False)
    except Exception as e:
        print('Error getting repo {}: {}'.format(args.repo, e))
        return

    # Verify the release exists
    try:
        release = None
        for r in repo.get_releases():
            if r.tag_name == args.version:
                release = r
                break
        if not release:
            print('Release {} not found'.format(args.version))
            return
    except Exception as e:
        print('Error getting release {}: {}'.format(args.version, e))
        return

    for asset in args.assets:
        try:
            release.upload_asset(asset)
            print('Uploaded {} to release {}'.format(asset, args.version))
        except Exception as e:
            print('Error uploading asset {}: {}'.format(asset, e))


if __name__ == '__main__':
    main()