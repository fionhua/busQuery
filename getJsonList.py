import os

def getJsonFile(dirname):
    result = []
    for maindir, subdir, file_name_list in os.walk(dirname):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            if apath.endswith('.json'):
                result.append(apath)
    return result