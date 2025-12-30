import requests
import json

SPREADSHEET_ID = '14-idXJHzHKCUQxxaqGZi-6S0G20gvPUhK4G16ci2FwI'
GID = '213021534'

def fetch_sheet_columns(gid):
    url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:json&gid={gid}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.text
        start_idx = content.find('(')
        end_idx = content.rfind(')')
        if start_idx != -1 and end_idx != -1:
            json_str = content[start_idx+1:end_idx]
            data = json.loads(json_str)
            
            if 'table' in data and 'cols' in data['table']:
                cols = data['table']['cols']
                labels = [c.get('label', '') for c in cols]
                print(f"GID {gid} Columns: {labels}")
                
                if 'rows' in data['table'] and len(data['table']['rows']) > 0:
                    # Print first 5 rows to see data samples (dates, statuses)
                    print(f"Sample Data (First 5 rows):")
                    for i, row in enumerate(data['table']['rows'][:5]):
                        values = [c.get('v', '') if c else '' for c in row.get('c', [])]
                        print(f"Row {i+1}: {values}")
            else:
                print(f"GID {gid}: No table/cols found.")
        else:
            print(f"GID {gid}: Could not parse JSON.")
    except Exception as e:
        print(f"GID {gid} Error: {e}")

fetch_sheet_columns(GID)
