#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import os
import signal

try:
    # Python 2
    input = raw_input
except NameError:
    pass

from app import app, queues, sched, _config, _enabled_jobs


def _teardown(signal, frame):
    sched.shutdown(wait=False)
    for queue in queues.values():
        queue.put(None)
    queues.clear()
    # Let the interrupt bubble up so that Flask/Werkzeug see it
    raise KeyboardInterrupt


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


def _run_app(debug=False):
    app.jinja_env.auto_reload = debug
    app.debug = debug
    signal.signal(signal.SIGINT, _teardown)
    host = os.environ.get('HOST', 'localhost')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port, use_reloader=False, threaded=True)


def main():
    parser = argparse.ArgumentParser(description='Helper script.')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true',
                        help='Run app in debug mode')
    parser.add_argument('-j', '--job', dest='job', action='store_true',
                        help='Run a job, will prompt if NAME is not given')
    parser.add_argument('-s', '--json', dest='json', action='store_true',
                        help='Print job output as JSON')
    parser.add_argument('name', metavar='NAME', nargs='?')
    args = parser.parse_args()

    if args.job:
        _run_job(args.name, args.json)
    else:
        _run_app(args.debug)


if __name__ == '__main__':
    main()
