import yaml 
import xml.etree.ElementTree as xml_tree 
with open('feed.yaml', 'r') as file: 
    yaml_data = yaml.safe_load(file) 
    rss_element = xml_tree.Element('rss', {
        'version': '2.0', 
        'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
        'xmlns:content': 'http://purl.org/rss/1.0/modules/content/'
    }) 

channel_element = xml_tree.SubElement(rss_element, 'channel') 
xml_tree.SubElement(channel_element, 'title').text = yaml_data['title'] 
output_tree = xml_tree.ElementTree(rss_element) 
output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)

# Continue adding elements to the channel based on the YAML data
xml_tree.SubElement(channel_element, 'link').text = yaml_data['link']
xml_tree.SubElement(channel_element, 'language').text = yaml_data['language']
xml_tree.SubElement(channel_element, 'copyright').text = yaml_data['copyright']
xml_tree.SubElement(channel_element, 'itunes:author').text = yaml_data['author']
xml_tree.SubElement(channel_element, 'description').text = yaml_data['description']
xml_tree.SubElement(channel_element, 'itunes:type').text = yaml_data['type']

# Add the image element
image_element = xml_tree.SubElement(channel_element, 'itunes:image', {
    'href': yaml_data['image']['href']
})

# Add categories
categories = yaml_data['categories']
for category in categories:
    category_element = xml_tree.SubElement(channel_element, 'itunes:category', {'text': category})
    subcategories = categories[category]
    for subcategory in subcategories:
        xml_tree.SubElement(category_element, 'itunes:category', {'text': subcategory})

# Add episodes
for episode in yaml_data['episodes']:
    item_element = xml_tree.SubElement(channel_element, 'item')
    xml_tree.SubElement(item_element, 'itunes:episodeType').text = episode['episodeType']
    xml_tree.SubElement(item_element, 'itunes:title').text = episode['title']
    xml_tree.SubElement(item_element, 'description').text = episode['description']
    xml_tree.SubElement(item_element, 'itunes:duration').text = str(episode['duration'])
    xml_tree.SubElement(item_element, 'itunes:explicit').text = str(episode['explicit']).lower()

    # Add enclosure details
    enclosure_element = xml_tree.SubElement(item_element, 'enclosure', {
        'url': episode['enclosure']['url'],
        'length': str(episode['enclosure']['length']),
        'type': episode['enclosure']['type']
    })

    # Add GUID and publication date
    xml_tree.SubElement(item_element, 'guid').text = episode['guid']
    xml_tree.SubElement(item_element, 'pubDate').text = episode['pubDate']

# Write the final RSS feed to an XML file
output_tree = xml_tree.ElementTree(rss_element)
output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)

# print("RSS feed has been successfully generated and saved as 'podcast.xml'.")
