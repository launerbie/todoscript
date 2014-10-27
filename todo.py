#!/usr/bin/env python

import argparse
import xml.etree.ElementTree as ET
import os
import configparser

def main():

    tree = ET.parse(TODOXML)
    tree.write(BACKUPXML)
    root = tree.getroot()

    def add():
        counter = int(root.attrib['counter'])
        root.set('counter', str(counter+1))

        task = ET.Element('task', attrib={'description':ARGS.todo_description,
                                          'priority': ARGS.priority,
                                          'id':str(counter),
                                          'archived':'false'
                                         })
        if ARGS.tags:
            for t in ARGS.tags:
                tag = ET.Element(t)
                task.append(tag)

        root.append(task)
        tree.write(TODOXML, xml_declaration=True)

    def remove():
        for task in root:
            if task.attrib['id'] == ARGS.item_ID:
                root.remove(task)
        tree.write(TODOXML)

    def list_items():
        if ARGS.archived is False:
            for task in root:
                if task.attrib['archived'] == 'false':
                    printer(task)
        else:
            for task in root:
                if task.attrib['archived'] == 'true':
                    printer(task)
        #TODO: sortyby

    def search():
        #TODO, although it seems unlikely that your todolist will become that long
        # that this is needed
        pass

    def archive():
        for task in root:
            if task.attrib['id'] == ARGS.item_ID:
                task.set('archived', 'true')
        tree.write(TODOXML)

    def update():
        #TODO
        pass

    commands = {
               'add':add,
               'remove':remove,
               'list':list_items,
               'search':search,
               'archive':archive,
               'update':update,
               }

    commands[ARGS.subcommand]()


def printer(task):
    task_id = task.attrib['id'].ljust(3)
    task_priority = task.attrib['priority'].ljust(8)
    task_descr = task.attrib['description']
    tags = " ".join(['['+child.tag+']' for child in task])
    print('{} {} {} {}'.format(task_id, task_priority, tags, task_descr))

def get_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand')

    add_parser = subparsers.add_parser('add', help='add item to todo list')
    add_parser.add_argument('todo_description')
    add_parser.add_argument('--tags', '-t', nargs='*')
    add_parser.add_argument('--priority', '-p', choices=['low', 'normal', 'high'], default='normal')

    remove_parser = subparsers.add_parser('remove', help='remove item from todo list')
    remove_parser.add_argument('item_ID')

    list_parser = subparsers.add_parser('list', help='list items')
    list_parser.add_argument('--sortby', choices=['date', 'description', 'priority'], default='priority')
    list_parser.add_argument('--archived', action='store_true')

    archive_parser = subparsers.add_parser('archive', help='archives an item')
    archive_parser.add_argument('item_ID')

    update_parser = subparsers.add_parser('update', help='update an item')
    update_parser.add_argument('item_ID')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    ARGS = get_args()
    HOME = os.environ['HOME']
    rcfile = HOME+'/.todorc'
    cfg = configparser.ConfigParser()
    cfg.read(rcfile)
    TODOXML = cfg['files']['todo']
    BACKUPXML = cfg['files']['backup']
    main()




