from datetime import datetime, timedelta
null=None

def check_path_end(path):
    if path.endswith("/"):
        path = path[:-1]
    return path

def strip_filename(filename):
    stripped=filename.rsplit('.', 1)[0]
    return stripped

def date_calc(days):
    date = datetime.today() - timedelta(days)
    return date.strftime("%Y-%m-%d")

def package_search(repo, path, days,timesetting):
    older_than = date_calc(days)
    path=check_path_end(path)
    args = [
        "items.find",
        {
            "type":"file",
            "repo" : repo,
            "path" : {"$match": path + "*"},
            "created" : {"$lt" : older_than},
            "$and" : [
                { "name": {"$nmatch" : "*.pom"}},
                { "name": {"$nmatch" : "*.xml"}},
                { "name": {"$nmatch" : "*.txt"}},
            ]
        },
    ]
    if timesetting == "since":
        args[1]['stat.downloaded']={"$lt" : older_than}
    elif timesetting == "older":
        args[1]['created']={"$lt" : older_than}
    else:
        args[1]['created']={"$lt" : older_than}
        args[1]['stat.downloads']={"$eq":null}

    return args

def file_search(repo, path, filename, days):
    name = strip_filename(filename)
    path=check_path_end(path)
    args = [
        "items.find",
        {
            "type":"file",
            "repo" : repo,
            "path" : {"$match": path + "*"},
            "name" : {"$match": name + "*"}
        },
        ".include", ["repo","path","name", "stat.downloads", "stat.downloaded"],
    ]
    return args

def check_file_list(files, days):
    older_than = date_calc(days)
    flag = False
    for file in files:
        if file['stats'][0]['downloads'] != 0:
            last_downlaod_date = file['stats'][0]['downloaded'].split('T')[0]
            if last_downlaod_date > older_than:
                flag = True
    return flag
