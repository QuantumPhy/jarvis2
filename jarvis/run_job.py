#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse

try:
    # Python 2
    input = raw_input
except NameError:
    pass

from app import _config, _enabled_jobs


def _run_job(job_id=None, print_json=False):
    import json
    import sys
    from jobs import load_jobs
    from pprint import pprint

    enabled_jobs = _enabled_jobs()
    jobs = load_jobs()

    if job_id is None or len(job_id) == 0:
        job_ids = ' '.join(enabled_jobs)
        job_id = input('Name of the job to run [%s]: ' % (job_ids,)).lower()

    job_config = _config().get(job_id)
    if job_config is None:
        print('No config found for job: %s' % (job_id,))
        sys.exit(1)

    cls = jobs.get(job_config.get('job_impl', job_id))
    if cls is None:
        print('No such job: %s' % (job_id,))
        sys.exit(1)

    job = cls(job_config)
    data = job.get()
    if print_json:
        print(json.dumps(data, indent=2))
    else:
        pprint(data)


def main():
    parser = argparse.ArgumentParser(
        description='Run given job and print output.'
    )
    parser.add_argument('-s', '--json', dest='json', action='store_true',
                        help='Print job output as JSON')
    parser.add_argument('name', metavar='NAME', nargs='?')
    args = parser.parse_args()

    _run_job(args.name, args.json)


if __name__ == '__main__':
    main()
