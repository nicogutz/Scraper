import json

with open("links.json", "r") as fp:
    file_list = json.load(fp)

set_files = set(x['dir'] for x in file_list)

set_files = [x for x in set_files]
set_files.sort()

with open("links_new.json", "w") as fp:
    json.dump(set_files, fp)
