# -*- coding: utf-8 -*-
from xml.sax.handler import ContentHandler
from xml.sax import parse
from itertools import combinations

from constants import AI_JOURNALS_AND_CONFERENCE

class Dispatcher:
    def dispatch(self, prefix, name, attrs=None):
        mname = prefix + name.capitalize()
        method = getattr(self, mname, None)

        if callable(method):
            if prefix == 'start': method(attrs)
            else: method()

    def startElement(self, name, attrs):
        self.dispatch('start', name, attrs)

    def endElement(self, name):
        self.dispatch('end', name)


class CoauthorMaker(Dispatcher, ContentHandler):
    def __init__(self):
        self.passthrough = False
        self.is_author = False
        self.coauthor_list = []

    def characters(self, chars):
        if self.passthrough and self.is_author:
            self.coauthor_list.append(chars)

    def startAuthor(self, attrs):
        self.is_author = True

    def endAuthor(self):
        self.is_author = False

    def startArticle(self, attrs):
        journals = attrs['key'].split('/')[1].upper()
        if AI_JOURNALS_AND_CONFERENCE.has_key(journals):
            self.passthrough = True
        else:
            print 'Not right journal'

    def endArticle(self):
        self.generate_paper_info()
        self.passthrough = False
        self.coauthor_list = []

    def startInproceedings(self, attrs):
        conf = attrs['key'].split('/')[1].upper()
        if AI_JOURNALS_AND_CONFERENCE.has_key(conf):
            self.passthrough = True
        else:
            print 'Not right conference'

    def endInproceedings(self):
        self.generate_paper_info()
        self.passthrough = False
        self.coauthor_list = []

    def generate_paper_info(self):
        with open('coauthor.csv', 'a') as f:
            if len(self.coauthor_list) < 2:
                print 'Only one author'
            else:
                for info in combinations(self.coauthor_list, 2):
                    f.write('{0}, {1}r\n'.format(info[0], info[1]))
                    print 'Write one piece of cooperation user'


parse('dblp.xml', CoauthorMaker())