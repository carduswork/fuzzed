import urllib, datetime

from django.core.mail import mail_managers

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from django.http import Http404

from openid2rp.django.auth import linkOpenID, preAuthenticate, AX, IncorrectClaimError
from FuzzEd.models import Graph, Project, Notification, notations, commands
import FuzzEd.settings

import logging
logger = logging.getLogger('FuzzEd')

GREETINGS = [
    'Loading the FuzzEd User Experience',
    'Trying to find your Data... it was here somewhere',
    'Fiddeling with your Graph... Stand by!',
    'Loading good Karma into your Browser',
    'Calculating the Answer to Life...',
    'Man, this takes like for ever to load...',
    'Time to grab some Coffee!'
]

def index(request):
    """
    Function: index
    
    This is the view handler for loading the landing page of the editor. The index.html is rendered unless the user is
    already signed in and being redirected to his or her dashboard.
    
    Parameters:
     {HttpRequest} request - a django request object
    
    Returns:
     {HttpResponse} a django response object
    """
    if 'logout' in request.GET:
        auth.logout(request)

    if request.user.is_authenticated():
        if 'next' in request.GET and len(request.GET['next']) > 0:
            return redirect(request.GET['next'])
        else:
            return redirect('projects')

    if 'next' in request.GET:
        # Makes this a hidden form parameter for the OpenID auth form submission
        return render(request, 'index.html', {'next': request.GET['next'], 'pwlogin': ('pwlogin' in request.GET)})
    else:
        return render(request, 'index.html', {'pwlogin': ('pwlogin' in request.GET)})

def about(request):
    """
    Function: about
    
    Simple rendering of the about page.
    
    Parameters:
     {HttpRequest} request - a django request
    
    Returns:
     {HttpResponse} a django response object
    """
    return render(request, 'util/about.html')
    
@login_required
def projects(request):
    """
    Function: projects
    
    This view handler renders a project overview containing all projects which are not marked as deleted, as well as in
    which the actual user is the owner or a project member. The resulting list of projects is ordered descending by its
    creation date. Also, a user is able to create a new project, as well as to delete a certain project if he is the owner.
    
    Parameters:
     {HttpRequest} request - a django request object
    
    Returns:
     {HttpResponse} a django response object
    """
    projects = (request.user.projects.filter(deleted=False) | request.user.own_projects.filter(deleted=False)).order_by('-created')

    parameters = {'projects':[ project.to_dict() for project in projects]}

    # provide notification box on the projects overview page, if something is available for this user
    try:
        notification = request.user.notification_set.latest('modified')
        parameters['notification'] = notification
    except:
        pass
            
    return render(request, 'project_menu/projects.html', parameters)
    
@login_required
def project_new(request):
    """
    Function: project_new
    
    This handler is responsible for rendering a dialog to the user to create a new project. It is also responsible for
    processing a save request of such a 'new project' request and forwards the user to the project overview site after doing so.
    
    Parameters:
     {HttpRequest} request - a django request object
    
    Returns:
     {HttpResponse} a django response object
    """
  
    if request.method == 'POST':
        POST = request.POST
        commands.AddProject.create_from(name=POST.get('name'), owner=request.user).do()
        return redirect('projects')
        
    return render(request, 'project_menu/project_new.html')
    
@login_required
def project_edit(request, project_id):
    """
    Function: project_edit
    
    This handler function is responsible for allowing the user to edit the properties of an already existing project.
    Therefore the system renders a edit dialog to the user where changes can be made and saved or the project can be
    deleted.
    
    Parameters:
     {HttpResponse} request    - a django request object
     {int}          project_id - the project to be edited
    
    Returns:
     {HttpResponse} a django response object
    """
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    POST  = request.POST

    # deletion requested? do it and go back to project overview
    if POST.get('delete'):
        commands.DeleteProject.create_from(project_id).do()
        messages.add_message(request, messages.SUCCESS, 'Project deleted.')
        return redirect('projects')
       
    # the owner made changes to the project's field, better save it (if we can)    
    elif POST.get('save'):
        project.name = POST.get('name', '')
        project.save()
        messages.add_message(request, messages.SUCCESS, 'Project saved.')
        return redirect('projects')
    
    # please show the edit page to the user on get requests
    elif POST.get('edit') or request.method == 'GET':
        parameters = {'project': project.to_dict()}
        return render(request, 'project_menu/project_edit.html', parameters)
    
    # something was not quite right here
    raise HttpResponseBadRequest()
        

@login_required
def dashboard(request, project_id):
    """
    Function: dashboard
    
    This view handler renders the dashboard in the context of a certain project. It lists all the graphs belonging to the project that are not marked as
    deleted ordered descending by its creation date. Also, a user is able to add new graphs to the project, as well as to edit or delete
    existing graphs from here.
    
    Parameters:
     {HttpRequest} request - a django request object
    
    Returns:
     {HttpResponse} a django response object
    """
    project = get_object_or_404(Project, pk=project_id)
    
    if not (project.is_authorized(request.user)):
        raise Http404
    
    # projects in which the actual user is owner or member and that were recently modified are proposed to the user
    proposal_limit =5
    project_proposals = Project.objects.filter(Q(deleted=False),Q(users = request.user)|Q(owner = request.user)).exclude(id=project.id).order_by('-modified')[:proposal_limit]
    
    graphs = project.graphs.filter(deleted=False).order_by('-created')
    parameters = {'graphs': [(notations.by_kind[graph.kind]['name'], graph) for graph in graphs],
                  'project': project.to_dict(),
                  'proposals': [ project.to_dict() for project in project_proposals]
                 }

    return render(request, 'dashboard/dashboard.html', parameters)

@login_required
def dashboard_new(request, project_id, kind):
    """
    Function: dashboard_new
    
    This handler is responsible for rendering a dialog to the user to create a new diagram. It is also responsible for
    processing a save request of such a 'new diagram' request and forwards the user to the dashboard after doing so.
    
    Parameters:
     {HttpRequest} request - a django http request object
    
    Returns:
     {HttpResponse} a django response object
    """
    project = get_object_or_404(Project, pk=project_id)
    
    # user can only create a graph if he is owner or member of the respective project
    if not (project.is_authorized(request.user)):
        raise Http404
        
    POST = request.POST

    # save the graph
    if POST.get('save') and POST.get('name'):
        commands.AddGraph.create_from(kind=kind, name=POST['name'], owner=request.user, project=project).do()
        return redirect('dashboard', project_id = project_id)

    # render the create diagram if fuzztree
    elif kind in notations.by_kind:
        parameters = {
            'kind': kind,
            'name': notations.by_kind[kind]['name'],
            'project' : project.to_dict()
        }
        return render(request, 'dashboard/dashboard_new.html', parameters)

    # something is not right with the request
    return HttpResponseBadRequest()

@login_required
def dashboard_edit(request, graph_id):
    """
    Function: dashboard_edit
    
    This handler function is responsible for allowing the user to edit the properties of an already existing graph.
    Therefore the system renders a edit dialog to the user where changes can be made and saved or the graph can be
    deleted.
    
    Parameters:
     {HttpResponse} request  - a django request object
     {int}          graph_id - the graph to be edited
    
    Returns:
     {HttpResponse} a django response object
    """
    graph = get_object_or_404(Graph, pk=graph_id, owner=request.user)
    project = graph.project
    
    POST  = request.POST

    # the owner made changes to the graph's field, better save it (if we can)
    if POST.get('save'):
        graph.name = POST.get('name', '')
        graph.save()
        messages.add_message(request, messages.SUCCESS, 'Graph saved.')
        return redirect('dashboard', project_id = project.id)

    # deletion requested? do it and go back to dashboard
    elif POST.get('delete'):
        commands.DeleteGraph.create_from(graph_id).do()
        messages.add_message(request, messages.SUCCESS, 'Graph deleted.')
        return redirect('dashboard', project_id = project.id)

    # copy requested
    elif POST.get('copy'):
        old_graph = Graph.objects.get(pk=graph_id)
        duplicate_command = commands.AddGraph.create_from(kind=old_graph.kind, name=old_graph.name + ' (copy)',
                                                          owner=request.user,  add_default_nodes=False, project=project)
        duplicate_command.do()
        new_graph = duplicate_command.graph

        new_graph.copy_values(old_graph)
        new_graph.save()

        messages.add_message(request, messages.SUCCESS, 'Graph duplicated.')
        return redirect('dashboard', project_id = project.id)

    elif POST.get('snapshot'):
        old_graph = Graph.objects.get(pk=graph_id)
        duplicate_command = commands.AddGraph.create_from(kind=old_graph.kind, name=old_graph.name + ' (snapshot)',
                                                          owner=request.user, add_default_nodes=False, project=project)
        duplicate_command.do()
        new_graph = duplicate_command.graph

        new_graph.copy_values(old_graph)
        new_graph.read_only = True
        new_graph.save()

        messages.add_message(request, messages.SUCCESS, 'Created snapshot.')
        return redirect('dashboard', project_id=project.id)


    # please show the edit page to the user on get requests
    elif POST.get('edit') or request.method == 'GET':
        parameters = {
            'graph': graph,
            'kind':  notations.by_kind[graph.kind]['name']
        }
        return render(request, 'dashboard/dashboard_edit.html', parameters)

    # something was not quite right here
    raise HttpResponseBadRequest()

@login_required
def settings(request):
    """
    Function: settings
    
    The view for the settings page. The code remembers the last page (e.g. project overview or project details) and goes
    backe to it afterwards.
   
    Parameters:
     {HttpRequest} request - a django request object
    
    Returns:
     {HttpResponse} a django response object
    """
    comes_from = request.META["HTTP_REFERER"]
    if 'settings' not in comes_from:
        request.session['comes_from']=comes_from
    POST = request.POST

    if POST.get('save'):
        user    = request.user
        profile = user.profile

        user.first_name    = POST.get('first_name', user.first_name)
        user.last_name     = POST.get('last_name', user.last_name)
        user.email         = POST.get('email', user.email)
        profile.newsletter = bool(POST.get('newsletter'))

        profile.save()
        user.save()

        messages.add_message(request, messages.SUCCESS, 'Settings saved.')
        return redirect(request.session['comes_from'])
    elif POST.get('generate'):
        from tastypie.models import ApiKey         
        user = request.user
        # User may be new, without any previous API key
        key = ApiKey.objects.get_or_create(user=user, defaults={'user': user})
        # Save new API key
        user.api_key.key = user.api_key.generate_key()
        user.api_key.save()
    elif POST.get('cancel'):
        return redirect(request.session['comes_from'])

    return render(request, 'util/settings.html')

@login_required
def editor(request, graph_id):
    """
    Function: editor
    
    View handler for loading the editor. It just tries to locate the graph to be opened in the editor and passes it to
    its according view.
    
    Parameters:
     {HttpRequest} request  - a django request object
     {int}         graph_id - the id of the graph to be opened in the editor
    
    Returns:
     {HttpResponse} a django response object
    """
    if request.user.is_staff:
        graph    = get_object_or_404(Graph, pk=graph_id)
    else:
        graph    = get_object_or_404(Graph, pk=graph_id, owner=request.user, deleted=False)
    if graph.read_only:
        return HttpResponseBadRequest()
    
    project  = graph.project     
    notation = notations.by_kind[graph.kind]
    nodes    = notation['nodes']

    parameters = {
        'graph':          graph,
        'graph_notation': notation,
        'nodes':          [(node, nodes[node]) for node in notation['shapeMenuNodeDisplayOrder']],
        'greetings':      GREETINGS, 
        'project' :       project.to_dict()
    }

    return render(request, 'editor/editor.html', parameters)

@login_required
def snapshot(request, graph_id):
    """
    Function: snapshot
    
    View handler for loading the snapshot viewer. It just tries to locate the graph to be opened 
    and passes it to its according view. For the moment, this is the editor itself, were the JavaScript
    code handles the read-only mode from UI perspective.
    
    Parameters:
     {HttpRequest} request  - a django request object
     {int}         graph_id - the id of the graph to be opened in the snapshot viewer
    
    Returns:
     {HttpResponse} a django response object
    """
    if request.user.is_staff:
        graph    = get_object_or_404(Graph, pk=graph_id)
    else:
        graph    = get_object_or_404(Graph, pk=graph_id, owner=request.user, deleted=False)
    if not graph.read_only:
        return HttpResponseBadRequest()

    project  = graph.project    
    notation = notations.by_kind[graph.kind]
    nodes    = notation['nodes']

    parameters = {
        'graph':          graph,
        'graph_notation': notation,
        'nodes':          [(node, nodes[node]) for node in notation['shapeMenuNodeDisplayOrder']],
        'greetings':      GREETINGS,
        'project':        project.to_dict()
    }

    return render(request, 'editor/editor.html', parameters)

@require_http_methods(['GET','POST'])
def login(request):
    """
    Function: login
    
    View handler for loging in a user using OpenID. If the user is not yet know to the system a new profile is created
    for him using his or her personal information as provided by the OpenID provider.

    The login view always redirects to the index view - and not directly to the project view - in order to keep
    the 'next' parameter handling in one place. Otherwise, the project view would need to consider the parameter too.
    
    Parameters:
     {HttpRequest} request - a django request object
    
    Returns:
     {HttpResponse} a django response object
    """
    GET = request.GET
    POST = request.POST

    # Consider the 'next' redirection
    if 'next' in request.GET:
        #TODO: Security issue ?
        redirect_params = '?next='+request.GET['next']
    else:
        redirect_params = ''

    # Ordinary password login. Since this is normally disabled in favour of OpenID login, all such users
    # got garbage passwords. This means that this code can remain in here as last ressort fallback for
    # the admin users that have real passwords.
    if 'loginname' in POST and 'loginpw' in POST:
        user = auth.authenticate(username=POST['loginname'], password=POST['loginpw'])
        # user found? sign-on
        if user is not None and user.is_active:
            auth.login(request, user)
        return redirect('/projects/'+redirect_params)

    elif 'openid_identifier' in POST:
        # first stage of OpenID authentication
        open_id = POST['openid_identifier']
        request.session['openid_identifier'] = open_id

        try:
            openidreturn = FuzzEd.settings.OPENID_RETURN
            if 'next' in request.POST:
                #TODO: Potential security problem
                openidreturn += '&next='+request.POST['next']
            logger.debug("OpenID return URL is "+openidreturn)
            return preAuthenticate(open_id, openidreturn)
        except IncorrectClaimError:
            messages.add_message(request, messages.ERROR, 'This OpenID claim is not valid.')
            return redirect('/'+redirect_params)

    elif 'openidreturn' in GET:
        user = auth.authenticate(openidrequest=request)

        if user.is_anonymous():    
            user_name = None
            email     = None

            user_sreg = user.openid_sreg
            user_ax   = user.openid_ax

            # not known to the backend so far, create it transparently
            if 'nickname' in user_sreg:
                user_name = unicode(user_sreg['nickname'], 'utf-8')[:29]
            else:
                now = datetime.datetime.now()
                user_name = 'Anonymous %d%d%d%d' % (now.hour, now.minute, now.second, now.microsecond)

            if 'email' in user_sreg:         
                email = unicode(user_sreg['email'], 'utf-8')[:29]

            if AX.email in user_ax:
                email = unicode(user_ax[AX.email], 'utf-8')[:29]

            # Google is using different claim IDs for the same user, if he comes
            # from different originating domains
            # This leads to a problem when user come from "www" or without "www"
            # We solve this by trusting the given email address as unique identifier
            if email:
                new_user, created = User.objects.get_or_create(email=email, defaults={'email':email, 'username':user_name})
            else:
                new_user = User(username=user_name)
                created = True

            if created:
                # Assign additional information to newly created User object
                if AX.first in user_ax:
                    new_user.first_name = unicode(user_ax[AX.first], 'utf-8')[:29]

                if AX.last in user_ax:
                    new_user.last_name=unicode(user_ax[AX.last], 'utf-8')[:29]

                mail_managers('New user', str(new_user), fail_silently=True)
                new_user.is_active = True
            else:
                mail_managers('New OpenID claim for user', str(new_user), fail_silently=True)

            new_user.save()

            linkOpenID(new_user, user.openid_claim) # especially relevant when user object was fetched, and not created
            
            return redirect('/login/?openid_identifier=%s' % urllib.quote_plus(request.session['openid_identifier'])) 
            
        auth.login(request, user)
    return redirect('/'+redirect_params)

