import re, os
pattern = re.compile('["\\\'][\\w /\\\\]+\\.\\w+["\']')

file_paths = []
data_files = []

for directory, folders, files in os.walk('..'):
    for file in files:
        file_path = os.path.join(directory, file)

        if file_path.startswith('.\\.git'):
            continue
        if file_path.startswith('.\\src\\__pycache__') or file_path.startswith('.\\__pycache__') or file_path.endswith('.pyc'):
            continue
        if file_path.startswith('.\\.idea'):
            continue

        print(file_path)

        if file_path.endswith(".py") or file_path.endswith('.json'):
            data_files.append(file_path)
        else:
            file_paths.append(file_path)

for i in data_files:
    with open(i) as f:
        print(i, end=' ')
        file_contents = f.read()
        matches = pattern.finditer(file_contents)
        num_removed = 0
        for match in matches:
            match_string = match.group()[1:-1]
            for j in range(len(file_paths)-1, -1, -1):
                try:
                    if os.path.samefile(match_string, file_paths[j]):
                        del file_paths[j]
                        num_removed+=1
                except FileNotFoundError:
                    print('error file:',i)
        print(num_removed)

for i in file_paths:
    print(i)


