#!/usr/bin/env python

import argparse
import jbox
import os

def create_galleries_args(args):
    gallery_list = [f.strip() for f in open(args.gallery_list).readlines()]
    create_galleries(gallery_list, args.target_dir, args.juicebox_src_dir)

def create_galleries(gallery_list, target_dir, juicebox_src_dir):
    common_prefix = os.path.commonprefix(gallery_list)
    for source_dir in gallery_list:
        gallery_name = os.path.basename(source_dir)
        jbox.create_gallery(
            source_dir, 
            os.path.join(target_dir, source_dir.strip('/')),
            "images", "thumbs",
            gallery_name,
            juicebox_src_dir)

def find_galleries_args(args):
    find_galleries(args.root_folder)

def find_galleries(root_folder):
    for dirpath, _, filenames in os.walk(root_folder):
        if os.path.basename(dirpath).find('.') != 0:
            extensions = map(lambda f: os.path.splitext(f)[1].lower(), filenames)
            if '.jpg' in extensions:
                print dirpath

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')

    create_galleries_parser = subparsers.add_parser('create_galleries')
    create_galleries_parser.add_argument('gallery_list')
    create_galleries_parser.add_argument('target_dir')
    create_galleries_parser.add_argument('juicebox_src_dir')
    create_galleries_parser.set_defaults(func=create_galleries_args)

    find_galleries_parser = subparsers.add_parser('find_galleries')
    find_galleries_parser.add_argument('root_folder')
    find_galleries_parser.set_defaults(func=find_galleries_args)

    args = parser.parse_args()
    args.func(args)
