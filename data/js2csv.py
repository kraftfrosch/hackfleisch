import json
import csv
import uuid

# Load your JSON data
with open('/Users/joshuakraft/Desktop/dev/hackfleisch/data/competency_framework.js', 'r') as f:
    data = json.load(f)

rows = []

# Process core competencies under 'department'
for dept_type, competencies in data[0]['department'].items():
    for comp in competencies:
        row = {
            'uuid': str(uuid.uuid4()),
            'type': 'core',
            'applicable_to': dept_type,
            'name': comp['name'],
            'description': comp['description'],
            'level_1': '\n'.join(comp['levels']['1']['description']),
            'level_2': '\n'.join(comp['levels']['2']['description']),
            'level_3': '\n'.join(comp['levels']['3']['description']),
            'level_4': '\n'.join(comp['levels']['4']['description']),
        }
        rows.append(row)

# Process functional competencies under 'roles'
for role, competencies in data[0]['roles'].items():
    for comp in competencies:
        row = {
            'uuid': str(uuid.uuid4()),
            'type': 'functional',
            'applicable_to': role,
            'name': comp['name'],
            'description': comp['description'],
            'level_1': '\n'.join(comp['levels']['1']['description']),
            'level_2': '\n'.join(comp['levels']['2']['description']),
            'level_3': '\n'.join(comp['levels']['3']['description']),
            'level_4': '\n'.join(comp['levels']['4']['description']),
        }
        rows.append(row)

# Write to CSV
with open('competence.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['uuid', 'type', 'applicable_to', 'name', 'description', 'level_1', 'level_2', 'level_3', 'level_4']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)