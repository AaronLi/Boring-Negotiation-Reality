import json, glob

for i in glob.iglob('*.json'):
    with open(i) as f:
        fInfo = json.load(f)

        fInfo['name'] = i.split('_')[0]

        fInfo['idle'] = 'game sprites/%s stand.png'%fInfo['name'].lower()

    with open(i,'w') as f:
        json.dump(fInfo, f, indent=True)