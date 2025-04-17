import json
import os

def generate_network_html(data, template_path, output_path):
    print(f"Generating network visualization from {template_path} to {output_path}")
    """
    Generate a network visualization HTML file from a template and data.
    
    Args:
        data: List of dictionaries containing network data
        template_path: Path to the HTML template file
        output_path: Path to write the output HTML file
    """
    # Convert data to JSON string
    data_json = json.dumps(data, ensure_ascii=False, indent=4)
    
    # Read the template file
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Replace the placeholder with the actual data
    output_content = template_content.replace('/* PLACEHOLDER_FOR_DATA */', data_json)
    
    # Write the output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_content)
    
    print(f"Generated network visualization at: {output_path}")

# Sample network data
network_data = [
    {"megbizo": "Állami Fejlesztési Központ", "megbizott": "Nagy Építő Kft.", "osszeg": 150000000, "palyazatokSzama": 2},
    {"megbizo": "Állami Fejlesztési Központ", "megbizott": "Gyors Projekt Zrt.", "osszeg": 85000000, "palyazatokSzama": 1},
    {"megbizo": "Városi Önkormányzat A", "megbizott": "Helyi Szolgáltató Bt.", "osszeg": 12000000, "palyazatokSzama": 5},
    {"megbizo": "Városi Önkormányzat A", "megbizott": "Nagy Építő Kft.", "osszeg": 250000000, "palyazatokSzama": 3},
    {"megbizo": "Kórház B", "megbizott": "Orvosi Műszer Kft.", "osszeg": 45000000, "palyazatokSzama": 8},
    {"megbizo": "Kórház B", "megbizott": "Tisztaság Expressz Zrt.", "osszeg": 8000000, "palyazatokSzama": 12},
    # Add more data entries as needed
    {"megbizo": "Városi Önkormányzat A", "megbizott": "Park Gondozó Kft.", "osszeg": 7000000, "palyazatokSzama": 8},
    {"megbizo": "Kórház B", "megbizott": "Nagy Építő Kft.", "osszeg": 90000000, "palyazatokSzama": 1},
]

# Paths
temp_path = '/home/mihaly/python_codes/kbsz/templates/network_template.html'
output_path = '/home/mihaly/python_codes/kbsz/temp_network.html'
# Generate HTML

generate_network_html(network_data, temp_path, output_path)