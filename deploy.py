# -*- coding: utf-8 -*-
"""
    Deployment script
"""
import argparse
import logging
import os
import subprocess


NAME = 'html-to-pdf'
CONF = {
    'dev': [
        {'project': '<project-id>', 'region': 'europe-west1'},
    ],
}


def run(env):
    for conf in CONF[env]:
        image = 'gcr.io/{}/{}'.format(conf['project'], NAME)

        command1 = ['gcloud',  'builds',  'submit']
        command1.extend(['--project', conf['project']])
        command1.extend(['--tag', image])

        command2 = ['gcloud', 'run', 'deploy', NAME]
        command2.extend(['--project', conf['project']])
        command2.extend(['--image', image])
        command2.extend(['--platform', 'managed'])
        command2.extend(['--no-allow-unauthenticated'])
        command2.extend(['--region', conf['region']])
        command2.extend(['--cpu', '1'])
        command2.extend(['--memory', '512Mi'])

        try:
            subprocess.check_call(command1, env=os.environ.copy())
            subprocess.check_call(command2, env=os.environ.copy())
        except subprocess.CalledProcessError:
            logging.error('Deploy failed.')
            exit(1)


def get_args():
    parser = argparse.ArgumentParser(description='Deployment script.')
    parser.add_argument('-e', '--env', '--environment', choices=['dev'],
                        default='dev', help='The environment to deploy on.')
    return parser.parse_args()


def main():
    args = get_args()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)
    run(args.env)


if __name__ == '__main__':
    main()
