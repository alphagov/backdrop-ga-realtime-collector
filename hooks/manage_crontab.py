import sys
import os


class ParseError(StandardError):
    pass

def generate_crontab(current_tab, job_path, path_to_app, path_to_python):
    job_template = '{schedule} {python} {app_path}/collect.py ' \
                   '-q {app_path}/{query} -c {app_path}/{config} ' \
                   '# {app_name}'

    app_name = "backdrop-ga-realtime-collector"
    crontab = [
        line.strip() for line in current_tab if ('# %s' % app_name) not in line
    ]
    with open(job_path) as jobs:
        try:
            for job in jobs:
                schedule, query, config = job.strip().split(",")

                cronjob = job_template.format(
                    schedule=schedule,
                    python=path_to_python,
                    app_path=path_to_app,
                    query=query,
                    config=config,
                    app_name=app_name
                )

                crontab.append(cronjob)
        except ValueError as e:
            raise ParseError(str(e))

    return crontab


if __name__ == "__main__":
    path_to_app = os.getenv("PATH_TO_APP")
    path_to_python = os.getenv("PATH_TO_PYTHON")

    job_path = os.path.join(os.path.dirname(__file__),
                            '..', 'config', 'cronjobs')

    try:
        crontab = generate_crontab(
            sys.stdin.readlines(),
            job_path,
            path_to_app,
            path_to_python
        )

        sys.stdout.write("\n".join(crontab) + "\n")
        sys.exit(0)
    except StandardError:
        sys.exit(1)