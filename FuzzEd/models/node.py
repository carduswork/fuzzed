from django.core.exceptions import ObjectDoesNotExist

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

import logging
logger = logging.getLogger('FuzzEd')

from xml_fuzztree import *
from graph import Graph

import json, notations, sys, time

def new_client_id():
    return str(int(time.mktime(time.gmtime())))

# TODO: CREATE ALL THE PROPERTIES OF THIS NODE ON CREATION (OR FACTORY METHOD?)

xml_classes = {
    'topEvent':             TopEvent,
    'basicEvent':           BasicEvent,
    'basicEventSet':        BasicEventSet,
    'intermediateEvent':    IntermediateEvent,
    'intermediateEventSet': IntermediateEventSet,
    'houseEvent':           HouseEvent,
    'undevelopedEvent':     UndevelopedEvent,
    'andGate':              And,
    'orGate':               Or,
    'xorGate':              Xor,
    'votingOrGate':         VotingOr,
    'featureVariation':     FeatureVariationPoint,
    'redundancyVariation':  RedundancyVariationPoint
}

class Node(models.Model):
    """
    Class: Node

    This class models a generic node for any diagram notation.

    Fields:
     {long}    client_id - an id for this node that is generated by the client
     {str}     kind      - a unique identifier for the kind of the node in its notation - e.g. "choice" for FuzzTrees.
                           Must be in the set of available node kinds of the owning graph's notation
     {<Graph>} graph     - the graph that owns the node
     {int}     x         - the x coordinate of the node (default: 0)
     {int}     y         - the y coordinate of the node (default: 0) 
     {bool}    deleted   - flag indicating whether this node is deleted. Simplifies restoration of nodes by toggling
                           the flag (default: False)
    """
    class Meta:
        app_label = 'FuzzEd'

    # Nodes that are created by the server (e.g. default nodes in the notation) should receive ids starting at
    # -sys.maxint and autoincrement from there on. The whole negative number range is reserved for the server. IDs from
    # the client MUST be zero or greater (usually UNIX timestamp in milliseconds from JS)
    client_id = models.BigIntegerField(default=-sys.maxint)
    kind      = models.CharField(max_length=127, choices=notations.node_choices)
    graph     = models.ForeignKey(Graph, null=False, related_name='nodes')
    x         = models.IntegerField(default=0)
    y         = models.IntegerField(default=0)
    deleted   = models.BooleanField(default=False)

    def __unicode__(self):
        prefix = '[DELETED] ' if self.deleted else ''

        try:
            name = unicode(self.properties.get(key='name').value)
            return unicode('%s%s' % (prefix, name))

        except ObjectDoesNotExist:
            return unicode('%s%s_%s' % (prefix, self.pk, notations.by_kind[self.graph.kind]['nodes'][self.kind]['name']))

    def to_json(self):
        """
        Method: to_json
        
        Serializes the values of this node into JSON notation.

        Returns:
         {str} the node in JSON representation
        """
        return json.dumps(self.to_dict())

    def to_dict(self):
        """
        Method: to_dict
        
        Serializes this node into a native dictionary
        
        Returns:
         {dict} the node as dictionary
        """
        serialized = dict([prop.to_tuple() for prop in self.properties.filter(deleted=False)])

        serialized['id']       = self.client_id
        serialized['kind']     = self.kind
        serialized['x']        = self.x
        serialized['y']        = self.y
        serialized['outgoing'] = [edge.client_id for edge in self.outgoing.filter(deleted=False)]
        serialized['incoming'] = [edge.client_id for edge in self.incoming.filter(deleted=False)]

        return serialized

    def to_bool_term(self):
        edges = self.outgoing.filter(deleted=False).all()
        children = []

        for edge in edges:
            children.append(edge.target.to_bool_term())

        if self.kind == 'orGate':
            return '(%s)' % (' or '.join(children))

        elif self.kind == 'andGate':
            return '(%s)' % (' and '.join(children))

        elif self.kind in ['basicEvent']:
            return str(self.client_id)

        elif self.kind == 'topEvent':
            return str(children[0])

        else:
            raise ValueError('Node %s has unsupported kind' % self)

    def to_xml(self):
        """
        Method: to_xml
        
        Serializes this node into an XML representation according to the schema file for the graph type. Please note
        the backend node ID is used instead of client_id, since the latter one is not globally unique and may be too
        long for some XML processors.
        
        Returns:
         This node instance
        """
        properties = {
            'id':   self.id,
            'name': self.get_property('name', '-')
        }

        if self.kind in {'basicEvent', 'basicEventSet', 'intermediateEvent', 'intermediateEventSet', 'houseEvent'}:
            properties['optional'] = self.get_property('optional', False)

        if self.kind in {'basicEvent', 'basicEventSet', 'houseEvent'}:
            probability = self.get_property('probability', None)
            if isinstance(probability, list):
                point = probability[0]
                alpha = probability[1]

                if alpha == 0:
                    properties['probability'] = CrispProbability(value_=point)
                else:
                    properties['probability'] = TriangularFuzzyInterval(a=point - alpha, b1=point,
                                                                        b2=point, c=point + alpha)

            elif isinstance(probability, long):
                properties['probability'] = CrispProbability(value_=probability)

            else:
                raise ValueError('Cannot handle probability value: "%s"' % probability)

            properties['costs'] = self.get_property('cost', 0)

        elif self.kind == 'votingOrGate':
            if self.graph.kind == 'fuzztree':
                properties['k'] = self.get_property('k')
            else:
                properties['k'] = self.get_property('kN')[0]

        elif self.kind == 'redundancyVariation':
            nRange = self.get_property('nRange')

            properties['start']   = nRange[0]
            properties['end']     = nRange[1]
            properties['formula'] = self.get_property('kFormula')

        try:
            xml_node = xml_classes[self.kind](**properties)
            logger.debug('[XML] Adding node "%s" with properties %s' % (self.kind, properties))

            # serialize children
            for edge in self.outgoing.filter(deleted=False):
                xml_node.children.append(edge.target.to_xml())

        except KeyError:
            raise ValueError('Unsupported node %s' % self.kind)

        return xml_node

    def get_property(self, key, default=None):
        try:
            return self.properties.get(key=key).value
        except ObjectDoesNotExist:
            try:
                logger.debug('Node has no property "%s", trying to use default from notation' % key)
                return notations.by_kind[self.graph.kind]['nodes'][self.kind][key]
            except KeyError:
                logger.debug('No default given in notation, assuming "%s" instead' % default)
                return default

    def get_attr(self, key):
        """
        Method: get_attr

        Use this method to fetch a node's attribute. It looks in the node object and its related properties.

        Parameters:
            {string} key - The name of the attribute.

        Returns:
            {attr} The found attribute. Raises a ValueError if no attribute for the given key exist.
        """
        if hasattr(self, key):
            return getattr(self, key)
        else:
            try:
                prop = self.properties.get(key=key)
                return prop.value
            except Exception:
                raise ValueError()

    def set_attr(self, key, value):
        """
        Method: set_attr

        Use this method to set a node's attribute. It looks in the node object and its related properties for an
        attribute with the given name and changes it. If non exist, a new property is added saving this attribute.

        Parameters:
            {string} key - The name of the attribute.
            {attr} value - The new value that should be stored.
        """
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            prop, created = self.properties.get_or_create(key=key)
            prop.value = value
            prop.save()

# the handler will ensure that the kind of the node is present in its containing graph notation
@receiver(pre_save, sender=Node)
def validate(sender, instance, raw, **kwargs):
    # raw is true if fixture loading happens, where the graph does not exist so far
    if not raw:
        graph = instance.graph
        if not instance.kind in notations.by_kind[graph.kind]['nodes']:
            raise ValueError('Graph %s does not support nodes of type %s' % (graph, instance.kind))

# ensures that the validate handler is not exported
__all__ = ['Node']
