import json

with open("waluigi_visual.json") as f:
    waInfo = json.load(f)

    waInfo['animations']['attack']['sprite_frames'] = ['A BNR/waluigi/attack/00%02d.png'%i for i in range(1,61)]

    waInfo['animations']['spell']['sprite_frames'] = ['A BNR/waluigi/attack/00%02d.png' % i for i in range(1, 61)]

    for i in range(4):
        waInfo['animations']['spell']['sprite_frames'].insert(i+49, 'A BNR/waluigi/spell%d.png'%i)


with open('waluigi_visual.json', 'w') as f:
    json.dump(waInfo, f, indent=True)