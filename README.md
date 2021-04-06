# python-artifactory-cleanup
Clean up Artifactory.

# Pre-requisite
It's based on [dohq-artifactory](https://github.com/devopshq/artifactory)

        pip install dohq-artifactory

# Installation
1. Clone the repository
2. Change conf/config.ini:


        [ARTIFACTORY]
        URL = __artifactory_url__
        API_KEY = __artifactory_apikey__

        [LOG]
        PATH = /var/log/python-artifactory-cleanup


# Command line options
      usage: main.py [-h] -r REPO -p PATH [-t TIME] [-d] [-v] [--show]

      Delete files from Artifactory

      optional arguments:
          -h, --help            show this help message and exit
          -r REPO, --repo REPO  Repository name
          -p PATH, --path PATH  Path to delete from
          -t TIME, --time TIME  Older than.... (days, optinal, default: 30)
          -s TIMESETTING, --timesetting TIMESETTING
                                [never|since|older]: used with time. Meanings: - never
                                downloaded AND older than [-t]. Since: not dowloaded
                                since [-t] days. Older: packages older than [-t] days
          -d, --delete          Default is dry run, must given if you want to delete
          -v, --verbose         Show files which are/could be deleted
          --show                Show only result
