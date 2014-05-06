import json
import logging

from django import http
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.core.urlresolvers import reverse
from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.shortcuts import get_object_or_404
from tastypie.authentication import SessionAuthentication
from tastypie.bundle import Bundle
from tastypie.http import HttpApplicationError, HttpAccepted
from tastypie import fields
from django.core.mail import mail_managers

from FuzzEd.decorators import require_ajax
from FuzzEd.models import Node, Job, NodeGroup, Graph
from FuzzEd.middleware import *
import common


logger = logging.getLogger('FuzzEd')

class JobResource(common.JobResource):
    """
        An API resource for jobs.
    """
    class Meta:
        queryset = Job.objects.all()
        authorization = common.GraphOwnerAuthorization()
        authentication = SessionAuthentication()        
        list_allowed_methods = ['post']
        detail_allowed_methods = ['get']

    graph = fields.ToOneField('FuzzEd.api.common.GraphResource', 'graph')

    def get_resource_uri(self, bundle_or_obj=None, url_name='api_dispatch_list'):
        """
            Since we change the API URL format to nested resources, we need also to
            change the location determination for a given resource object.
        """
        job_secret = bundle_or_obj.obj.secret
        graph_pk = bundle_or_obj.obj.graph.pk
        return reverse('job', kwargs={'api_name':'front', 'pk':graph_pk, 'secret':job_secret})

    def obj_create(self, bundle, **kwargs):
        """
            Create a new job for the given graph.
            The request body contains the information about the kind of job being requested.
            The result is a job URL that is based on the generated job secret.
            This is the only override that allows us to access 'kwargs', which contains the
            graph_id from the original request.
        """
        graph = Graph.objects.get(pk=kwargs['graph_id'], deleted=False)
        bundle.data['graph'] = graph
        bundle.data['graph_modified'] = graph.modified
        bundle.data['kind'] = bundle.data['kind']
        bundle.obj = self._meta.object_class()
        bundle = self.full_hydrate(bundle)
        return self.save(bundle)

    def get_detail(self, request, **kwargs):
        """
            Called by the request dispatcher in case somebody tries to GET a job resource.
            For the frontend, deliver the current job status if pending, or the result.
        """
        basic_bundle = self.build_bundle(request=request)
        try:
            job = self.cached_obj_get(bundle=basic_bundle, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return http.HttpNotFound()
        except MultipleObjectsReturned:
            return http.HttpMultipleChoices("More than one resource is found at this URI.")

        if job.done():
            if job.exit_code == 0:
                return job.as_http_response()
            else:
                logger.debug("Job is done, but with non-zero exit code.")
                mail_managers('Analysis of job %s ended with non-zero exit code.' % job.pk, job.graph.to_xml())
                return HttpApplicationError()
        else:
            # Job is pending, tell this by HTTP return code
            return HttpAccepted()

    def apply_authorization_limits(self, request, object_list):
        # Prevent cross-checking of jobs by different users
        return object_list.filter(graph__owner=request.user)                    

class NotificationResource(common.NotificationResource):
    class Meta(common.NotificationResource.Meta):
        authentication = SessionAuthentication()

class NodeResource(common.NodeResource):
    class Meta(common.NodeResource.Meta):
        authentication = SessionAuthentication()

class EdgeResource(common.EdgeResource):
    class Meta(common.EdgeResource.Meta):
        authentication = SessionAuthentication()

class ProjectResource(common.ProjectResource):
    class Meta(common.ProjectResource.Meta):
        authentication = SessionAuthentication()

class GraphSerializer(common.GraphSerializer):
    """
        The frontend gets its own JSON format for the graph information,
        not the default HATEOAS format generated by Tastypie. For this reason,
        we need a frontend API specific JSON serializer.
    """
    def to_json(self, data, options=None):
        if isinstance(data, Bundle):
            return data.obj.to_json()
        else:
            graphs = []
            for graph in data['objects']:
                graphs.append({'url': reverse('graph', kwargs={'api_name': 'front', 'pk': graph.obj.pk}),
                               'name': graph.obj.name})
            return json.dumps({'graphs': graphs})


class GraphResource(common.GraphResource):
    """
        Override our GraphResource Meta class to register the custom
        frontend JSON serializer and the frontent auth method.
    """
    class Meta(common.GraphResource.Meta):
        authentication = SessionAuthentication()
        serializer = GraphSerializer()

    def dispatch_edges(self, request, **kwargs):
        edge_resource = EdgeResource()
        return edge_resource.dispatch_list(request, graph_id=kwargs['pk'])

    def dispatch_edge(self, request, **kwargs):
        edge_resource = EdgeResource()
        return edge_resource.dispatch_detail(request, graph_id=kwargs['pk'], client_id=kwargs['client_id'])

    def dispatch_nodes(self, request, **kwargs):
        node_resource = NodeResource()
        return node_resource.dispatch_list(request, graph_id=kwargs['pk'])

    def dispatch_node(self, request, **kwargs):
        node_resource = NodeResource()
        return node_resource.dispatch_detail(request, graph_id=kwargs['pk'], client_id=kwargs['client_id'])

    def dispatch_jobs(self, request, **kwargs):
        job_resource = JobResource()
        return job_resource.dispatch_list(request, graph_id=kwargs['pk'])

    def dispatch_job(self, request, **kwargs):
        job_resource = JobResource()
        return job_resource.dispatch_detail(request, graph_id=kwargs['pk'], secret=kwargs['secret'])

@login_required
@csrf_exempt
@require_ajax
@require_GET
def graph_transfers(request, graph_id):
    """
    Function: graph_transfers

    Returns a list of transfers for the given graph

    Request Parameters: graph_id = <INT>
    Response:           200 - <TRANSFERS_AS_JSON>

    Parameters:
     {HTTPRequest} request  - the django request object
     {int}         graph_id - the id of the graph to get the transfers for

    Returns:
     {HTTPResponse} a django response object
    """
    transfers = []
    if request.user.is_staff:
        graph     = get_object_or_404(Graph, pk=graph_id)
    else:
        graph     = get_object_or_404(Graph, pk=graph_id, owner=request.user, deleted=False)        

    if graph.kind in ['faulttree', 'fuzztree']:
        for transfer in Graph.objects.filter(~Q(pk=graph_id), owner=request.user, kind=graph.kind, deleted=False):
            transfers.append({'id': transfer.pk, 'name': transfer.name})

    return HttpResponse(json.dumps({'transfers': transfers}), 'application/javascript', status=200)

@login_required
@csrf_exempt
@require_ajax
@require_POST
@never_cache
def nodegroups(request, graph_id):        

    if request.user.is_staff:
        graph = get_object_or_404(Graph, pk=graph_id)
    else:
        graph = get_object_or_404(Graph, pk=graph_id, owner=request.user, deleted=False)
    if graph.read_only:
        raise HttpResponseForbiddenAnswer('Trying to create a node in a read-only graph')

    nodeids = json.loads(request.POST['nodeIds'])
    client_id = request.POST['id']
    group = NodeGroup(client_id = client_id, graph=graph)
    group.save()        # Prepare ManyToMany relationship
    for nodeid in nodeids:
        try:
            # The client may refer to nodes that are already gone,
            # we simply ignore them
            node = Node.objects.get(pk = nodeid, deleted = False)
            group.nodes.add(node)
        except:
            pass
    group.save()    

    response = HttpResponse(group.to_json(), 'application/javascript', status=201)
    response['Location'] = reverse('nodegroup', args=[graph_id, group.client_id])
    return response

@login_required
@csrf_exempt
@require_ajax
@never_cache
def nodegroup(request, graph_id, group_id):
    try:
        group = get_object_or_404(NodeGroup, client_id=group_id, graph__pk=graph_id)

        if group.graph.read_only:
            raise HttpResponseForbiddenAnswer('Trying to modify a node in a read-only graph')

        if request.method == 'DELETE':
            group.deleted = True
            group.save()
            return HttpResponse(status=204)

    except Exception as exception:
        logger.error('Exception: ' + str(exception))
        raise exception


