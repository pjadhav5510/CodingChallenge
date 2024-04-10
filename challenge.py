import argparse
import json
import os
import sys
import xml.etree.ElementTree as ET

def parse_xml(file_path):
    addresses = []
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        for person in root.findall('person'):
            address = {}
            address['name'] = person.find('name').text
            address['street'] = person.find('address/street').text
            address['city'] = person.find('address/city').text
            address['county'] = person.find('address/county').text
            address['state'] = person.find('address/state').text
            address['zip'] = person.find('address/zip').text
            addresses.append(address)
    except Exception as e:
        print(f"Error parsing XML file {file_path}: {e}", file=sys.stderr)
    return addresses

def parse_tsv(file_path):
    addresses = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split('\t')
                if len(parts) >= 5:
                    address = {}
                    address['name'] = parts[0]
                    address['organization'] = parts[1]
                    address['street'] = parts[2]
                    address['city'] = parts[3]
                    address['state'] = parts[4]
                    if len(parts) == 6:
                        address['zip'] = parts[5]
                    addresses.append(address)
                else:
                    print(f"Error: Insufficient fields in TSV file {file_path}", file=sys.stderr)
    except Exception as e:
        print(f"Error parsing TSV file {file_path}: {e}", file=sys.stderr)
    return addresses

def parse_txt(file_path):
    addresses = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            print(lines)
            print('***************************************************')
            for i in range(2, len(lines), 3):  # Each record is separated by 4 lines
                name = lines[i].strip()
                #print('------------------------------------------------------------------------------------------------',name, 'i : ',i)
                street = lines[i + 1].strip()
                #print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++',street, 'i : ',i)
                #if lines[i + 2].isnumeric():
                if any(c.isdigit() for c in lines[i + 2]):
                    print(True, ' : ', lines[i + 2])
                else:
                    print(False, ' : ', lines[i + 2])
                city_state_zip = lines[i + 2].strip().split()
                #print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&',city_state_zip, 'i : ',i)
                if len(city_state_zip) >= 3:
                    city = city_state_zip[0]
                    state = city_state_zip[1]
                    zip_code = city_state_zip[2]
                    county = ''
                    if len(city_state_zip) > 3:
                        county = ' '.join(city_state_zip[3:])
                    address = {
                        'name': name,
                        'street': street,
                        'city': city,
                        'state': state,
                        'zip': zip_code,
                        'county': county
                    }
                    addresses.append(address)
                else:
                    print(f"Error: Insufficient fields in TXT file {file_path}", file=sys.stderr)
    except Exception as e:
        print(f"Error parsing TXT file {file_path}: {e}", file=sys.stderr)
    return addresses


def parse_file(file_path):
    _, ext = os.path.splitext(file_path)
    if ext == '.xml':
        return parse_xml(file_path)
    elif ext == '.tsv':
        return parse_tsv(file_path)
    elif ext == '.txt':
        return parse_txt(file_path)
    else:
        print(f"Error: Unsupported file format {ext} for file {file_path}", file=sys.stderr)
        return []

def main():
    parser = argparse.ArgumentParser(description="Parse US names and addresses from various file formats and output as JSON")
    parser.add_argument("files", metavar="FILE", type=str, nargs="+", help="Input file(s) to parse")
    
    try:
        args = parser.parse_args()
        addresses = []
        for file_path in args.files:
            addresses.extend(parse_file(file_path))
        
        if addresses:
            addresses.sort(key=lambda x: x.get('zip', ''))
            print(json.dumps(addresses, indent=2))
        else:
            sys.exit(1)
    except argparse.ArgumentError as e:
        print(f"Argument Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
