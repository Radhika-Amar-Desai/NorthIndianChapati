from bs4 import BeautifulSoup
import json

# Load the menu.html content
with open('menu.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Load the menu.json content
with open('menu.json', 'r', encoding='utf-8') as file:
    menu_json = json.load(file)

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Group JSON dishes by heading then dish name for quick lookup
json_dishes_map = {}
for item in menu_json:
    heading = item['heading']
    dish = item['dish']
    if heading not in json_dishes_map:
        json_dishes_map[heading] = {}
    json_dishes_map[heading][dish] = item

# Iterate over all h2 headings in HTML (categories)
for h2 in soup.find_all('h2'):
    heading_text = h2.text.strip()

    # Look for dishes under this heading (h3 until next h2)
    next_node = h2.find_next_sibling()
    while next_node and next_node.name != 'h2':
        if next_node.name == 'h3':
            dish_name = next_node.text.strip()
            # Find matching dish in JSON
            dish_data = json_dishes_map.get(heading_text, {}).get(dish_name)
            if dish_data:
                # Next expected nodes are price and description paragraphs
                price_tag = next_node.find_next_sibling()
                desc_tag = price_tag.find_next_sibling() if price_tag else None

                # Update price if tag exists
                if price_tag and price_tag.name == 'p':
                    price_tag.string = f"Rs. {dish_data['price']}"

                # Update description if tag exists
                if desc_tag and desc_tag.name == 'p':
                    desc_tag.string = dish_data.get('description', '')

        next_node = next_node.find_next_sibling()

# Save updated soup to new_menu.html
with open('new_menu.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))
