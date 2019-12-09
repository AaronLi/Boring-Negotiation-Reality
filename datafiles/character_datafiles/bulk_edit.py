import json, glob

for i in glob.iglob('*.json'):
    with open(i) as f:
        fInfo = json.load(f)
        fInfo['name'] = fInfo['name'].title()

    with open(i,'w') as f:
        json.dump(fInfo, f, indent=True)