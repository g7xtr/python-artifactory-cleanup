import aql_search
import sys
import argparse
import configparser
from datetime import datetime
from artifactory import ArtifactoryPath
from datetime import datetime
import timeit
run_start = timeit.default_timer()
config = configparser.ConfigParser()
config.read('conf/config.ini')
art_apikey = config.get('ARTIFACTORY', 'API_KEY')
art_url = config.get('ARTIFACTORY', 'URL')
log_path = config.get('LOG', 'PATH')

parser = argparse.ArgumentParser(description='Delete files from Artifactory')
parser.add_argument('-r','--repo', type=str, required=True, help='Repository name')
parser.add_argument('-p', '--path', type=str, required=True, help='Path to delete from')
parser.add_argument('-t', '--time', type=int, default=30, help='Older than.... (days, optinal, default: 30)')
parser.add_argument('-d','--delete', action='store_true', help='Default is dry run, must given if you want to delete')
parser.add_argument('-v', '--verbose', action='store_true', help='Show files which are/could be deleted')
parser.add_argument('--show', action='store_true', help='Show only result')

try:
    options = parser.parse_args()
except:
    sys.exit(0)

repo = options.repo
path = options.path
days = options.time
delete = options.delete
verbose = options.verbose

aql = ArtifactoryPath(
    art_url,
    apikey=art_apikey
)

args = aql_search.package_search(repo, path,days)
artifacts_list = aql.aql(*args)
if options.show:
    print(len(artifacts_list))
    exit()

total_file_count = 0
if delete:
    log_name = log_path + "/log-deleting-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".log"
else:
    log_name = log_path + "/log-dry_run-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".log"

log_file = open(log_name, 'w')

for item in artifacts_list:
    file_args=aql_search.file_search(repo, path, item["name"])
    file_list= aql.aql(*file_args)

    for file in file_list:
        file_url = art_url + file['repo'] + "/" + file['path'] + "/" + file['name']
        full_path = ArtifactoryPath(file_url,apikey=art_apikey)
        total_file_count += 1

        if delete:
            if full_path.exists():
                log_msg = "deleting: " + file_url
                full_path.unlink()
        else:
            log_msg = "dry run: " + file_url

        if verbose:
            print(log_msg)
        log_file.write(log_msg + "\n")

run_stop = timeit.default_timer()
running_time = run_stop - run_start
log_msg_total = "   # packages: "+ str(len(artifacts_list)) + "\n   # files:    " + str(total_file_count) + "\n Running time: " + str(running_time)
log_file.write(log_msg_total + "\n")
log_file.close()

print(log_msg_total)
