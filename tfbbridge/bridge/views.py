from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from .models import Organization
import requests

auth_link = "https://oauth.groupme.com/oauth/authorize?client_id=qAAAc8GSUlTA8C3Ypo9CMiFQwQCQnU8zPU5KGEtz3FYHDqP5"

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def handle_send_requests(token, org_id):
    # firstly, check what organization the org_id belongs to
    matching = Organization.objects.filter(_sender_url = org_id)
    if matching == []:
        return HttpResponseBadRequest # this is a fake org_id

def handle_oauth(request):
    token = request.GET.get('access_token')
    try:
        request_type = request.session["type"]
        organization_id = request.session["id"]
    except KeyError:
        return HttpResponseBadRequest

    if request_type == "send":
        return handle_send_requests(token, organization_id)

    return HttpResponse(token)

def add_sending_group(request, url_id):
    # first part -- authenticate with the GroupMe api
    request.session['type'] = "send"
    request.session['id'] = url_id

    return redirect(auth_link)