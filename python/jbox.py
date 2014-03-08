#!/usr/bin/env python

import argparse
import os
from PIL import Image, ImageOps

def create_config_xml(gallery_name, images):
    def gallery(gallery_name, images):
        return '''<juiceboxgallery 

    resizeOnImport="false"
    galleryTitle="%s"
    useFullscreenExpand="true"
    useThumbDots="false">

%s

</juiceboxgallery>''' % (gallery_name, '\n'.join(images))

    def image(img_path, thumbnail_path, source, img_title="", img_caption=""):
        return '''        <image imageURL="%s"
            thumbURL="%s"
            linkURL="%s"
            linkTarget="_blank"
            sourcePath="%s">
            <title><![CDATA[%s]]></title>
            <caption><![CDATA[%s]]></caption>
        </image>''' % (img_path, thumbnail_path, img_path, source, img_title, img_caption)

    images = (image(**img) for img in images)
    return '''<?xml version="1.0" encoding="UTF-8"?>
%s''' % gallery(gallery_name, images)

default_extensions = ['.jpeg', '.jpg', '.gif', '.png']

def find_images(gallery_dir, extensions=None):
    '''Searches for all jpgs in gallery dir and returns an array of image paths'''
    def is_image(filename, extensions):
        _, ext = os.path.splitext(filename)
        return ext.lower() in extensions

    gallery_dir = os.path.realpath(gallery_dir)
    if not extensions:
        extensions = [ext.lower() for ext in default_extensions]
    paths = []
    for dirpath, _, filenames in os.walk(gallery_dir):
        for filename in filenames:
                if is_image(filename, extensions):
                    paths.append(os.path.relpath(os.path.join(dirpath, filename), gallery_dir))
    return paths

def create_thumbnail(source_image, target_image, width, height):
    size = width, height

    # target_image = os.path.splitext(infile)[0] + ".thumbnail"
    if source_image != target_image:
        try:
            im = Image.open(source_image)
            thumb = ImageOps.fit(im, size, Image.ANTIALIAS)
            thumb.save(target_image, "JPEG")
        except IOError as e:
            print e
            print "cannot create copy for '%s'" % source_image

def resize_image(source_image, target_image, width, height):
    if source_image != target_image:
        try:
            img = Image.open(source_image)
            wpercent = (width/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((width,hsize), Image.ANTIALIAS)
            img.save(target_image)
        except IOError as e:
            print e
            print "cannot create copy for '%s'" % source_image

def prepare_images(source_dir, target_dir, target_image_dir, target_thumbnail_dir):
    '''Transform the image path array into an array of dicts containing img_path, thumbnail_path, img_title and img_caption'''
    images = []
    for image_path in find_images(source_dir):
        source_image = os.path.join(source_dir, image_path)
        target_thumbnail = os.path.join(target_thumbnail_dir, image_path)
        target_image = os.path.join(target_image_dir, image_path)
        try:
            os.makedirs(os.path.join(target, os.path.dirname(target_thumbnail)))
        except:
            pass
        try:
            os.makedirs(os.path.join(target, os.path.dirname(target_image)))
        except:
            pass
        create_thumbnail(source_image, os.path.join(target, target_thumbnail), 85, 85)
        resize_image(source_image, os.path.join(target, target_image), 1024, 768)
        image_title = os.path.splitext(os.path.basename(image_path))[0]
        images.append({
            'img_path': target_image,
            'thumbnail_path': target_thumbnail,
            'img_title': image_title,
            'img_caption': '',
            'source': source_image
        })
    return images

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('source_dir')
    parser.add_argument('target_dir')
    parser.add_argument('-i', '--images-dir', default='images')
    parser.add_argument('-t', '--thumbnails-dir', default='thumbs')
    args = parser.parse_args()

    gallery_dir = args.source_dir
    target = args.target_dir
    images = prepare_images(gallery_dir, target, args.images_dir, args.thumbnails_dir)

    with open(os.path.join(target, 'config.xml'), 'w') as f:
        f.write(create_config_xml('gallery_name', images))

