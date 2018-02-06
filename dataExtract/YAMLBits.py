#!/bin/env python

import yaml
import os
import re

class FormIdentifierOffset(yaml.YAMLObject):
        yaml_tag = u'!Offset'
        def __init__(self, xcorner, ycorner):
                self.X = xcorner
                self.Y = ycorner
        def __repr__(self):
                return "%s, %s" % ( self.X, self.Y )
        def getMinCoord(self):
                return (self.X.getMin(), self.Y.getMin())
        def getMaxCoord(self):
                return (self.X.getMax(), self.Y.getMax())

class FormIdentifierExtent(yaml.YAMLObject):
        yaml_tag = u'!Extent'
        def __init__(self, start, extent):
                self.start = start
                self.extent = extent
        def __repr__(self):
                return "%d %+d" % (self.start, self.extent)
        def getMax(self):
                return self.start+self.extent
        def getMin(self):
                return self.start
        
class FormIdentifierAnchor(yaml.YAMLObject):
        yaml_tag = u'!Anchor'
        def __init__( self, a, b ):
                self.Left = a
                self.Top = b
        def __repr__(self):
                return "%s, %s" % ( self.Left, self.Top )

class FormIdentifierData(yaml.YAMLObject):
        yaml_tag = u'!Identifier'
        def __init__(self, name, offsets, anchor, coordRange):
                self.name = name
                self.offsets = offsets
                self.anchor = anchor
                self.coordRange = coordRange
        def __repr__(self):
                return "%s(name=%s, offsets=%s)" % (
                        self.__class__.__name__, self.name, self.offsets )
        def getOffsets(self):
                if type(self.offsets) is list:
                        rl = []
                        for offset in self.offsets:
                                rl.append( offset.__repr__() )
                        return rl
                else:
                        return [ offset.__repr__() ]

class YAMLSetup(object):
        @classmethod
        def extent_repr( cls, dumper, data ):
                return dumper.represent_scalar(u'!Extent', u'%s' % data )
        @classmethod
        def extent_constructor( cls, loader, node ):
                val = loader.construct_scalar(node)
                split_regex = re.compile( r'\s+' )
                s, e = map( int, split_regex.split(val) )
                return FormIdentifierExtent(s,e)
        @classmethod
        def anchor_repr(cls, dumper, data):
                return dumper.represent_scalar(u'!Anchor', u'%s' % data )
        @classmethod
        def anchor_constructor( cls, loader, node ):
                val = loader.construct_scalar(node)
                x, y = val.split('!')
                return FormIdentifierAnchor(x,y)
        @classmethod
        def setup(cls):
                yaml.add_representer(FormIdentifierExtent, cls.extent_repr)
                yaml.add_constructor(u'!Extent', cls.extent_constructor)
                ex_rex = re.compile(r'^\d+\s+[\+\-]\d+$')
                yaml.add_implicit_resolver(u'!Extent', ex_rex)
                
class YAML:
    def __init__(self):
        YAMLSetup().setup()

    def load(self, filename):
        fn = os.path.expanduser(filename)
        fn = os.path.expandvars(fn)
        fn = os.path.abspath(fn)
        if os.path.exists(fn) is True:
            with open( fn, 'r' ) as stream:
                try:
                    rd = yaml.load( stream )
                    return rd
                except yaml.YAMLError as exc:
                        if hasattr(exc, 'problem_mark'):
                                extra = "Error at position %s:%s" % (exc.problem_mark.line+1,
                                                                     exc.problem_mark.column+1)
                        else:
                                extra = None
                        msg = "Error loading %s (%s): %s" % (filename, fn, exc)
                        if extra is not None:
                                msg += "\n%s" % extra
                        print msg
                        return None
        else:
            print "File %s (%s) does not exist!" % (filename, fn)
            return None

    def load_string(self, data):
        try:
            rd = yaml.load( data )
        except yaml.YAMLError as exc:
                if hasattr(exc, 'problem_mark'):
                        extra = "Error at position %s:%s" % (exc.problem_mark.line+1,
                                                             exc.problem_mark.column+1)
                else:
                        extra = None
                        msg = "Error parsing input stream: %s" % exc
                        if extra is not None:
                                msg += "\n%s" % extra
                        print msg
                        return None
                rd = None
        return rd
    
