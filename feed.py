import yaml
import xml.etree.ElementTree as xml_tree

# Load the YAML file
with open('feed.yaml', 'r') as file:
    yaml_data = yaml.safe_load(file)

# Create the root RSS element
rss_element = xml_tree.Element('rss', {
    'version': '2.0',
    'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
    'xmlns:content': 'http://purl.org/rss/1.0/modules/content/'
})

# Add the channel element
channel_element = xml_tree.SubElement(rss_element, 'channel')

# Populate the channel metadata
xml_tree.SubElement(channel_element, 'title').text = yaml_data['title']
xml_tree.SubElement(channel_element, 'language').text = yaml_data.get('language', 'en-us')
xml_tree.SubElement(channel_element, 'itunes:author').text = yaml_data['author']
xml_tree.SubElement(channel_element, 'description').text = yaml_data['description']

# Add image metadata
if 'image' in yaml_data:
    xml_tree.SubElement(channel_element, 'itunes:image', {'href': yaml_data['image']})

# Add categories
if 'category' in yaml_data:
    xml_tree.SubElement(channel_element, 'itunes:category', {'text': yaml_data['category']})

# Add items (episodes)
if 'item' in yaml_data:
    for episode in yaml_data['item']:
        item_element = xml_tree.SubElement(channel_element, 'item')
        xml_tree.SubElement(item_element, 'title').text = episode['title']
        xml_tree.SubElement(item_element, 'description').text = episode['description']
        xml_tree.SubElement(item_element, 'pubDate').text = episode['published']
        xml_tree.SubElement(item_element, 'itunes:duration').text = episode['duration']

        # Add enclosure
        enclosure_element = xml_tree.SubElement(item_element, 'enclosure', {
            'url': episode['file'],
            'length': str(episode['length']),
            'type': yaml_data.get('format', 'audio/mpeg')  # Default to audio/mpeg
        })

# Write the RSS feed to an XML file
output_tree = xml_tree.ElementTree(rss_element)
output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)

print("RSS feed has been successfully generated and saved as 'podcast.xml'.")
