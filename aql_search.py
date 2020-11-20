from datetime import datetime, timedelta
null=None

def check_path_end(path):
    if path.endswith("/"):
        path = path[:-1]
    return path

def strip_filename(filename):
    stripped=filename.rsplit('.', 1)[0]
    return stripped

def package_search(repo, path, days):
    path=check_path_end(path)
    older_than = datetime.today() - timedelta(days)
    older_than = older_than.strftime("%Y-%m-%d")
    path_widecard = '/*'
    if path == '/':
        path_widecard = '*'
    args = [
        "items.find",
        {
            "type":"file",
            "stat.downloads":{"$eq":null},
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
    return args

def file_search(repo, path, filename):
    name = strip_filename(filename)
    path=check_path_end(path)
    args = [
        "items.find",
        {
            "type":"file",
            "repo" : repo,
            "path" : {"$match": path + "/*"},
            "name" : {"$match": name + "*"}
        },
        ".include", ["repo","path","name"],
    ]
    return args
