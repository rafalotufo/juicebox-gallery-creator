#!/usr/bin/env python

import xml.etree.ElementTree as ET
import argparse
import os
import shutil

'''
create gallery index
'''

def decode(s):
    try:
        return s.encode('ascii', 'ignore')
    except:
        return 'can\'t decode'

def get_gallery_name(config_file):
    
    return doc.attrib['galleryTitle']

def find_galleries(root_path):
    for dirpath, _, filenames in os.walk(root_path):
        if 'config.xml' in filenames and 'index.html' in filenames:
            config_file = os.path.join(dirpath, 'config.xml')
            doc = ET.parse(config_file).getroot()
            gallery_name = doc.attrib['galleryTitle']
            image = os.path.join(dirpath, doc.getchildren()[1].attrib['imageURL'])
            yield {
                'name': gallery_name,
                'path': dirpath.replace(root_path + '/', ''),
 fdså2                'image': image.replace(root_path + '/', '')
            }

def create_index(galleries):
    gallery_list = ''
    for gallery in galleries:
        gallery_list += '''

    <div class="gallery">
        <a data-overlayer="effect:bottom;invert:on;" href="%s/index.html">
            <img class="gallery-thumbnail" src="%s" alt="" />
            <div class="overlay"><h3><strong>%s</strong></h3></div>
        </a>
    </div>
        
    ''' % (encode(gallery['path']), encode(gallery['image']), encode(gallery['name']))

    head = '''
<script type="text/javascript" src="asset/jquery.js"></script>
<script type="text/javascript" src="asset/jQuery.easing.js"></script>
<script type="text/javascript" src="asset/jQuery.thumbFx.js"></script>
<link href="http://fonts.googleapis.com/css?family=Open+Sans+Condensed:700,300,300italic" rel="stylesheet" type="text/css">
<link href="asset/all.css" rel="stylesheet" type="text/css">

<style>
body {
    background-color: black;
    color: white;
}
.gallery {
    float: left;
    margin: 5px;
}

.gallery-thumbnail {
    width: 200px;
}

</style>
'''

    return '''<html>
    <head>
%s
    </head>
    <body>
%s
    </body>
</html>
    ''' % (head, gallery_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('root_folder')
    # parser.add_argument('target')
    parser.add_argument('assets_dir')
    args = parser.parse_args()

    galleries = find_galleries(args.root_folder)
    try:
        shutil.copytree(args.assets_dir, os.path.join(args.root_folder, 'asset'))
    except:
        print 'Could not copy assets, probably already exists'
    with open(os.path.join(args.root_folder, 'index.html'), 'w') as f:
        f.write(create_index(galleries).encode('ascii', 'ignore'))
