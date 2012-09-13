from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.conf import settings
from new_tracker.models import new_request,UserProfile, request_owners, request_attachment
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.utils.simplejson import loads, JSONEncoder
from django.http import HttpResponse
from django.db.models.query import QuerySet
from django.template import RequestContext
import datetime
from django.contrib.auth.models import User
from new_tracker.extend_json import DjangoJSONEncoder
from django.utils import simplejson



media_url=settings.MEDIA_URL  #media_url for the path of media directory from settings file

""" Class for converting QuerySet object to JSON serializable 

"""
class ComplexEncoder( JSONEncoder ):
    def default( self, obj ):
        if isinstance( self, QuerySet ):
            return loads( serializers.serialize( 'json', obj ))
        return JSONEncoder.default( self, obj )
    

@login_required
def index(request):
    context_instance = RequestContext(request)
    user_data = request.user.get_profile()
    dept = user_data.department
    
    all_users = User.objects.all()
    template_values = {'MEDIA_URL':media_url, 'request': context_instance,'dept': dept, 'all_users': all_users }
    return render_to_response("new_request_submitted.html", template_values)

@login_required
def view_page(request):
    request_id = request.GET['request_id']
    all_info = new_request.objects.select_related().filter( id = request_id )
    request_owner_names = request_owners.objects.filter( new_request = request_id )
    template_values = { 'MEDIA_URL':media_url, 'all_info': all_info, 'request_owner_names': request_owner_names }
    return render_to_response("view_page.html", template_values )
    
@login_required
def create_new(request):
    context_instance = RequestContext(request)
    user_data = request.user.get_profile()
    dept = user_data.department
    current_date = datetime.date.today()
    current_date = current_date.strftime("%d-%m-%Y")
    all_users = User.objects.all()
    template_values = {'MEDIA_URL':media_url, 'creation_date':current_date, 'request': context_instance,'dept': dept, 'all_users': all_users }
    return render_to_response("index.html", template_values)
    

"""Function for handling new request.

"""
@login_required
@csrf_exempt
def create_new_request(request):
    context_instance = RequestContext(request)
    current_date = datetime.datetime.now()
    current_date = current_date.strftime("%d-%m-%Y")
    
    modified_date = datetime.datetime.now()
    modified_date = modified_date.strftime("%a %b %d %Y %H:%M:%S")

    post_data = request.POST.copy()
    extra_assignees = request.POST.getlist('user_added')
    total_users = request.POST.getlist('database_users')

    
    primary_assignees = post_data['ticketowner']
    attachment =  post_data['attach_file']
    
    create_new_request = new_request()
    create_new_request.title = post_data['title']
    create_new_request.creator = request.user
    create_new_request.primary_assignee = primary_assignees
    create_new_request.department = post_data['department']
    create_new_request.status = post_data['status']
    create_new_request.priority = post_data['pri_radio']
    create_new_request.severity = post_data['sev_radio']
    
    upper_case_user = str(request.user).capitalize()
    posted_decsription = "<b>"+ upper_case_user + " has requested on " + modified_date +":<br /></b>" +post_data['description']
    create_new_request.description = posted_decsription
    create_new_request.creation_date = current_date
    create_new_request.last_modified_date = current_date
    create_new_request.attachment = attachment
    create_new_request.save()
    
    
    for names in extra_assignees:
        request_owner_names = request_owners()
        request_owner_names.new_request_id = create_new_request.id
        request_owner_names.request_owner = names
        request_owner_names.save()
    
    template_values = { 'MEDIA_URL': media_url,'request':context_instance,'request_id': create_new_request.id }
  
    if str(attachment) == 'True':
        return render_to_response("file_upload.html", template_values)
    else:
        return render_to_response("new_request_submitted.html", template_values)
        
    
"""Function to upload the attachment.

"""
@login_required
@csrf_exempt
def upload_file(request):
    context_instance = RequestContext(request)
    posted_data = request.POST.copy()
    posted_data.update(request.FILES)
    request_id = posted_data['request_id']
    attachment1 = posted_data['attachment1']
    attachment2 = posted_data['attachment2']
    attachment3 = posted_data['attachment3']
    attachment4 = posted_data['attachment4']
    attachment5 = posted_data['attachment5']
    attachment6 = posted_data['attachment6']
    attachment7 = posted_data['attachment7']
    attachment8 = posted_data['attachment8']
    attachment9 = posted_data['attachment9']
    attachment10 = posted_data['attachment10']
    
    #all_request_info = new_request.objects.select_related().get(id=request_id)
    all_attachment_id = request_attachment.objects.all().values_list('new_request', flat = True)
    
    #request_id = 17
    
    if int(request_id) in list(all_attachment_id):
        pass
    else:
        request_attachment_model = request_attachment()
        request_attachment_model.new_request_id = request_id
        request_attachment_model.attachment1 = attachment1
        request_attachment_model.attachment2 = attachment2
        request_attachment_model.attachment3 = attachment3
        request_attachment_model.attachment4 = attachment4
        request_attachment_model.attachment5 = attachment5
        request_attachment_model.attachment6 = attachment6
        request_attachment_model.attachment7 = attachment7
        request_attachment_model.attachment8 = attachment8
        request_attachment_model.attachment9 = attachment9
        request_attachment_model.attachment10 = attachment10
        request_attachment_model.save()
    template_values = { 'MEDIA_URL': media_url,'request':context_instance,'request_id': request_id }
    return render_to_response("new_request_submitted.html", template_values)
    
    

"""Function for retrieving page to update the existing request.

"""
@login_required
@csrf_exempt
def update_request_page(request):
    request_id = request.GET['request_id']
    all_request_info = new_request.objects.get( id=request_id )
    all_owners_info = all_request_info.request_owners_set.all()
    all_uploaded_file = all_request_info.request_attachment_set.all()
    all_users = User.objects.all()
    current_date = datetime.datetime.now()
    current_date = current_date.strftime("%d-%m-%Y")
   
    template_values = { 'MEDIA_URL': media_url, "all_request_info": all_request_info,'all_users': all_users, 'all_owners_info':all_owners_info }
    return render_to_response("update_request_page.html", template_values)
  

"""Function to update the user changed values in database.

"""
@login_required
@csrf_exempt
def update_request(request):
    context_instance = RequestContext(request)
    current_date = datetime.datetime.now()
    current_date = current_date.strftime("%d-%m-%Y")
    
    modified_date = datetime.datetime.now()
    modified_date = modified_date.strftime("%a %b %d %Y %H:%M:%S")
    
    extra_assignees = request.POST.getlist('user_added')
    total_users = request.POST.getlist('database_users')

    extra_assignees = list(extra_assignees)
    
    
    post_data = request.POST.copy()
    primary_assignees = post_data['ticketowner']
    attachment =  post_data['attach_file']
    #extra_assignees.append(primary_assignees)
    request_id = post_data['request_id']
    update_request = new_request.objects.get( id=request_id )
    update_request.title = post_data['title']
    update_request.creator = post_data['creator']
    #update_request.request_owner = extra_assignees
    update_request.primary_assignee = primary_assignees
    update_request.department = post_data['department']
    #update_request.status = post_data['status']
    update_request.priority = post_data['priority']
    update_request.severity = post_data['severity']
    update_request.description = post_data['description']
    #update_request.creation_date = post_data['creation_date']
    #update_request.last_modified_date = current_date  
    update_request.save()
    
    
    request_owner_names = request_owners.objects.filter( new_request = update_request.id ).delete()
    
    for names in extra_assignees:
        request_owner_names = request_owners()
        request_owner_names.new_request_id = update_request.id
        request_owner_names.request_owner = names
        request_owner_names.save()
    
    
    update_attachment = update_request.request_attachment_set.all()
  
    template_values = { 'MEDIA_URL': media_url, 'request':context_instance, 'request_id': request_id, 'update_attachment': update_attachment }
    #return render_to_response("new_request_submitted.html", template_values)
    
    if str(attachment) == 'True':
        return render_to_response("attachment_update.html", template_values)
    else:
        return render_to_response("new_request_submitted.html", template_values)

@login_required
@csrf_exempt    
def update_attachment(request):
    context_instance = RequestContext(request)
    posted_data = request.POST.copy()
    posted_data.update(request.FILES)
    request_id = posted_data['request_id']
    #update_attachment = all_request.request_attachment_set.all()
    update_attachment = request_attachment.objects.get( new_request = request_id )
    
    attachment1 = posted_data['attachment1']
    attachment2 = posted_data['attachment2']
    attachment3 = posted_data['attachment3']
    attachment4 = posted_data['attachment4']
    attachment5 = posted_data['attachment5']
    attachment6 = posted_data['attachment6']
    attachment7 = posted_data['attachment7']
    attachment8 = posted_data['attachment8']
    attachment9 = posted_data['attachment9']
    attachment10 = posted_data['attachment10']
    
    if attachment1:
        update_attachment.attachment1.delete()
        update_attachment.new_request_id = request_id
        update_attachment.attachment1 = attachment1
        update_attachment.save()
    
    if attachment2:
        update_attachment.attachment2.delete()
        update_attachment.new_request_id = request_id
        update_attachment.attachment2 = attachment2
        update_attachment.save()
    
    if attachment3:
        update_attachment.attachment3.delete()
        update_attachment.new_request_id = request_id
        update_attachment.attachment3 = attachment3
        update_attachment.save()
  
    if attachment4:
        update_attachment.attachment4.delete()
        update_attachment.new_request_id = request_id
        update_attachment.attachment4 = attachment4
        update_attachment.save()
    
    if attachment5:
        update_attachment.attachment5.delete()
        update_attachment.new_request_id = request_id
        update_attachment.attachment5 = attachment5
        update_attachment.save()
        
    if attachment6:
        update_attachment.attachment6.delete()
        update_attachment.new_request_id = request_id
        update_attachment.attachment6= attachment6
        update_attachment.save()
        
    if attachment7:
        update_attachment.attachment7.delete()
        update_attachment.new_request_id = request_id
        update_attachment.attachment7 = attachment7
        update_attachment.save()
        
    if attachment8:
        update_attachment.attachment8.delete()
        update_attachment.new_request_id = request_id
        update_attachment.attachment8 = attachment8
        update_attachment.save()
    
    if attachment9:
        update_attachment.attachment9.delete()
        update_attachment.new_request_id = request_id
        update_attachment.attachment9 = attachment9
        update_attachment.save()
        
    if attachment10:
        update_attachment.attachment10.delete()
        update_attachment.new_request_id = request_id
        update_attachment.attachment10 = attachment10
        update_attachment.save()
    
    template_values = { 'MEDIA_URL': media_url, 'request':context_instance, 'request_id': request_id }
    return render_to_response("new_request_submitted.html", template_values)

"""This function is for showing the attachment.

"""   
@login_required
@csrf_exempt    
def show_attachment(request):
    #posted_data = request.POST.copy()
    #request_id = posted_data['request_id']
    request_id = request.GET['request_id']
    all_request_info = new_request.objects.get( id=request_id )
    all_uploaded_file = all_request_info.request_attachment_set.all()
    
    #total_file = all_request_info.request_attachment_set.all().count()
    template_values = { 'MEDIA_URL': media_url,'all_uploaded_file': all_uploaded_file  }
    return render_to_response('show_attachment.html', template_values)
    
  
   
"""Get all the data submitted by this user and show on the new_request_submitted page.

"""
@csrf_exempt
def get_all_user_request(request):
    result = {}
    result['all_user_request'] = new_request.objects.select_related().filter( creator = request.user )
    
        
    total_request_id = new_request.objects.filter( creator = request.user ).values_list('id', flat= True)

    count_dict = {}
    
    
    for requests in total_request_id:
        total_count = 0
        all_request_info = new_request.objects.select_related().get( id=requests )
        #count_dict[requests] = all_request_info.request_attachment_set.all()
        all_attachments = all_request_info.request_attachment_set.all()
        
        for attachments in all_attachments:
            if attachments.attachment1:
                total_count = total_count + 1
        
            if attachments.attachment2:
                total_count = total_count + 1
        
            if attachments.attachment3:
                total_count = total_count + 1
        
            if  attachments.attachment4:
                total_count = total_count + 1
        
            if attachments.attachment5:
                total_count = total_count + 1
            
            if attachments.attachment6:
                total_count = total_count + 1
            
            if attachments.attachment7:
                total_count = total_count + 1
            
            if attachments.attachment8:
                total_count = total_count + 1
        
            if attachments.attachment9:
                total_count = total_count + 1
        
            if attachments.attachment10:
                total_count = total_count + 1
        
            count_dict[requests] = total_count
        
        
    result['total_count'] = count_dict
    
    all_user_request = []
    all_user_request.append(result)
        
   
    format  = 'json'
    mimetype = "application/json"
    
    #all_user_request = serializers.serialize(format, all_user_request)
    
    all_user_request = simplejson.dumps(all_user_request, cls=DjangoJSONEncoder)
    
    
    return HttpResponse( all_user_request, mimetype )

   
   
"""Get all request user is assignee.


@csrf_exempt
def get_all_assigned_request(request):
    
    all_requests = new_request.objects.all()
    user_data = User.objects.all()
    
    
    format  = 'json'
    mimetype = "application/json"
    
    
    for user in user_data:
        if str(user.username) == str(request.user):
            first_name = user.first_name
            last_name = user.last_name
    name = first_name+' '+last_name
    
    owner_request = request_owners.objects.filter( request_owner = name ).values_list('new_request_id', flat= True)    
    

    assigned_request = new_request.objects.select_related().filter( id__in = owner_request )
 
    #assigned_request = [ myrequest for myrequest in assigned_request if str(name) in str( myrequest.request_owner ) ]
    
    assigned_request = serializers.serialize( format, assigned_request )
    
    return HttpResponse( assigned_request, mimetype )
"""

@csrf_exempt
def get_all_assigned_request(request):
    all_requests = new_request.objects.all()
    user_data = User.objects.all()

    format  = 'json'
    mimetype = "application/json"
    
    
    for user in user_data:
        if str(user.username) == str(request.user):
            first_name = user.first_name
            last_name = user.last_name
    name = first_name+' '+last_name
    
    result = {}
    
    owner_request = request_owners.objects.filter( request_owner = name ).values_list('new_request_id', flat= True)    
    
    result['assigned_request'] = new_request.objects.filter( id__in = owner_request )
    
    #result['assigned_request'] = assigned_request
    
    total_request_id = new_request.objects.filter( id__in = owner_request ).values_list('id', flat= True)
    
    count_dict = {}
    
    for requests in total_request_id:
        total_count = 0
        all_request_info = new_request.objects.get( id=requests )
        #count_dict['count'] = int(all_request_info.request_attachment_set.all().count())
        all_attachments = all_request_info.request_attachment_set.all()
        for attachments in all_attachments:
            if attachments.attachment1:
                total_count = total_count + 1
        
            if attachments.attachment2:
                total_count = total_count + 1
        
            if attachments.attachment3:
                total_count = total_count + 1
        
            if  attachments.attachment4:
                total_count = total_count + 1
        
            if attachments.attachment5:
                total_count = total_count + 1
            
            if attachments.attachment6:
                total_count = total_count + 1
            
            if attachments.attachment7:
                total_count = total_count + 1
            
            if attachments.attachment8:
                total_count = total_count + 1
        
            if attachments.attachment9:
                total_count = total_count + 1
        
            if attachments.attachment10:
                total_count = total_count + 1
        
            count_dict[requests] = total_count
    
    result['total_count'] = count_dict
    
    assigned_request = []
    assigned_request.append(result)
    
    assigned_request = simplejson.dumps(assigned_request, cls=DjangoJSONEncoder)
    
    return HttpResponse( assigned_request, mimetype )


"""Get all request where user is primary assignee.


@csrf_exempt
def get_all_primary_assigned_request(request):
    
    all_primary_requests = new_request.objects.all()
    
    user_data = User.objects.all()
    for user in user_data:
        if str(user.username) == str(request.user):
            first_name = user.first_name
            last_name = user.last_name
    name = first_name+' '+last_name
    
    format  = 'json'
    mimetype = "application/json"
    
    all_primary_requests = [ myrequest for myrequest in all_primary_requests if str(name) in str(myrequest.primary_assignee) ]
    
    all_primary_requests = serializers.serialize(format, all_primary_requests)
    
    return HttpResponse( all_primary_requests, mimetype )
"""

@csrf_exempt
def get_all_primary_assigned_request(request):
    
    all_requests = new_request.objects.all()
    user_data = User.objects.all()
    for user in user_data:
        if str(user.username) == str(request.user):
            first_name = user.first_name
            last_name = user.last_name
    name = first_name+' '+last_name
    
    format  = 'json'
    mimetype = "application/json"
    
    
    #all_primary_requests = [ myrequest for myrequest in all_requests if str(name) in str(myrequest.primary_assignee) ]
    all_primary_requests = new_request.objects.filter(primary_assignee = name)
    
    result = {}
    result['all_primary_requests'] = all_primary_requests
    #total_request_id = new_request.objects.filter(primary_assignee = name).values_list('id', flat= True)
    
    
    total_request_id = []
    for requests in all_primary_requests:
        total_request_id.append(requests.id)
    
    count_dict = {}
    
    for requests in total_request_id:
        total_count = 0
        all_request_info = new_request.objects.get( id=requests )
        #count_dict['count'] = int(all_request_info.request_attachment_set.all().count())
        all_attachments = all_request_info.request_attachment_set.all()
        for attachments in all_attachments:
            if attachments.attachment1:
                total_count = total_count + 1
        
            if attachments.attachment2:
                total_count = total_count + 1
        
            if attachments.attachment3:
                total_count = total_count + 1
        
            if  attachments.attachment4:
                total_count = total_count + 1
        
            if attachments.attachment5:
                total_count = total_count + 1
            
            if attachments.attachment6:
                total_count = total_count + 1
            
            if attachments.attachment7:
                total_count = total_count + 1
            
            if attachments.attachment8:
                total_count = total_count + 1
        
            if attachments.attachment9:
                total_count = total_count + 1
        
            if attachments.attachment10:
                total_count = total_count + 1
        
            count_dict[requests] = total_count
        
    result['total_count'] = count_dict
    
    primary_assigned_request = []
    primary_assigned_request.append(result)
   
    primary_assigned_request = simplejson.dumps(primary_assigned_request, cls=DjangoJSONEncoder)
    
    return HttpResponse( primary_assigned_request, mimetype )

"""Function to edit the request by users

"""
@login_required
@csrf_exempt
def edit_form(request):
    request_id = request.GET['request_id']
    user_data = request.user.get_profile()
    admin = user_data.admin
    template_values = { 'MEDIA_URL': media_url, 'request_id': request_id,'admin': admin }
    return render_to_response("edit_form.html", template_values)

"""Function to submit the comment by users.
    
"""
@login_required
@csrf_exempt
def edit_comment(request):
    current_date = datetime.datetime.now()
    current_date = current_date.strftime("%d-%m-%Y")
    
    modified_date = datetime.datetime.now()
    modified_date = modified_date.strftime("%a %b %d %Y %H:%M:%S")
    
    upper_case_user = str(request.user).capitalize()    
    post_data = request.POST.copy()
    comment = post_data['comment']
    request_id = post_data['request_id']
    edit_request = new_request.objects.get( id=request_id )
    old_description = edit_request.description 
    edit_request.description = "<br /><b>"+upper_case_user+" has updated on "+modified_date + ":<br /></b>"+comment+'<br />'+old_description
    edit_request.last_modified_date = current_date 
    edit_request.save()
    template_values = { 'MEDIA_URL': media_url }
    return render_to_response("new_request_submitted.html", template_values)


"""Function to create new users.
    
"""
@login_required
@csrf_exempt
def create_user(request):
    template_values={'MEDIA_URL':media_url}
    return render_to_response("registration/create_user_form.html",template_values)

@csrf_exempt
def checkusername(request):
    user_name = request.POST.get('user_name', False)
    if user_name:
        u = User.objects.filter(username=user_name).count()
        if u != 0:
            res = "<html><body><font color='red'>Already account exist</font></body></html>"
        else:
            res = "<html><body><font color='green'>OK</font></body></html>"
    else:
        res = ""

    return HttpResponse('%s' % res)

@login_required
@csrf_exempt
def create_login(request):
    template_values={'MEDIA_URL':media_url}
    if request.method=='POST':
        data=request.POST.copy()
        User.username=data['user_name']
        first_name=data['first_name']
        last_name=data['last_name']
        User.email=data['email_address']
        User.password=data['password']
        name=User.username
        
        try:
            user=User.objects.get(username=name)
            return render_to_response("registration/user_exist.html",template_values)
        except User.DoesNotExist:
            user= User.objects.create_user(name,User.email,User.password)
            user.first_name=first_name
            user.last_name=last_name
            user.save()
            userprofile=UserProfile()
            userprofile.user = user
            userprofile.department=data['dept']
            userprofile.admin=data['admin']
            userprofile.save()
    return render_to_response("registration/create_successful.html",template_values)
    
    
    

    


    
