#!/usr/bin/env python
# TODO: Upload to GitHub releases
# TODO: .pypirc configuration
from __future__ import print_function

import argparse
import json
import os
import os.path
import shutil
import subprocess

from six.moves.urllib.parse import urljoin
from six.moves.urllib.request import urlopen
from twine.commands import upload


APPVEYOR_API_BASE_URL = 'https://ci.appveyor.com/api/'
APPVEYOR_API_PROJECT_URL = urljoin(APPVEYOR_API_BASE_URL,
                                   'projects/dahlia/libsass-python/')
APPVEYOR_API_BUILDS_URL = urljoin(APPVEYOR_API_PROJECT_URL,
                                  'history?recordsNumber=50&branch=master')
APPVEYOR_API_JOBS_URL = urljoin(APPVEYOR_API_PROJECT_URL,
                                'build/')
APPVEYOR_API_JOB_URL = urljoin(APPVEYOR_API_BASE_URL, 'buildjobs/')


def ci_builds():
    response = urlopen(APPVEYOR_API_BUILDS_URL)
    projects = json.loads(response.read().decode('utf-8'))  # py3 compat
    response.close()
    return projects['builds']


def ci_tag_build(tag):
    builds = ci_builds()
    commit_id = git_tags().get(tag)
    for build in builds:
        if build['isTag'] and build['tag'] == tag:
            return build
        elif build['commitId'] == commit_id:
            return build


def git_tags():
    try:
        tags = subprocess.check_output(['git', 'tag'])
    except subprocess.CalledProcessError:
        return {}

    def read(tag):
        command = ['git', 'rev-list', tag]
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        try:
            firstline = p.stdout.readline()
        finally:
            p.terminate()
        return firstline.decode().strip()
    return {tag: read(tag) for tag in tags.decode().split()}


def ci_jobs(build):
    url = urljoin(APPVEYOR_API_JOBS_URL, build['version'])
    response = urlopen(url)
    build = json.loads(response.read().decode('utf-8'))  # py3 compat
    response.close()
    return build['build']['jobs']


def ci_artifacts(job):
    url = urljoin(urljoin(APPVEYOR_API_JOB_URL, job['jobId'] + '/'),
                  'artifacts/')
    response = urlopen(url)
    files = json.loads(response.read().decode('utf-8'))  # py3 compat
    response.close()
    for file_ in files:
        file_['url'] = urljoin(url, file_['fileName'])
    return files


def download_artifact(artifact, target_dir, overwrite=False):
    print('Downloading {0}...'.format(artifact['fileName']))
    response = urlopen(artifact['url'])
    filename = os.path.basename(artifact['fileName'])
    target_path = os.path.join(target_dir, filename)
    if os.path.isfile(target_path) and \
       os.path.getsize(target_path) == artifact['size']:
        if overwrite:
            print(artifact['fileName'], ' already exists; overwrite...')
        else:
            print(artifact['fileName'], ' already exists; skip...')
            return target_path
    with open(target_path, 'wb') as f:
        shutil.copyfileobj(response, f)
        assert f.tell() == artifact['size']
    response.close()
    return target_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--overwrite', action='store_true', default=False,
                        help='Overwrite files if already exist')
    parser.add_argument('--dist-dir', default='./dist/',
                        help='The temporary directory to download artifacts')
    parser.add_argument(
        'tag',
        help=('Git tag of the version to upload.  If it has a leading slash, '
              'it means AppVeyor build number rather than Git tag.')
    )
    args = parser.parse_args()
    if args.tag.startswith('/'):
        build = {'version': args.tag.lstrip('/')}
    else:
        build = ci_tag_build(args.tag)
    jobs = ci_jobs(build)
    if not os.path.isdir(args.dist_dir):
        print(args.dist_dir, 'does not exist yet; creating a new directory...')
        os.makedirs(args.dist_dir)
    dists = []
    for job in jobs:
        artifacts = ci_artifacts(job)
        for artifact in artifacts:
            dist = download_artifact(artifact, args.dist_dir, args.overwrite)
            dists.append(dist)
    print('Uploading {0} file(s)...'.format(len(dists)))
    upload.main(('-r', 'pypi') + tuple(dists))


if __name__ == '__main__':
    main()
