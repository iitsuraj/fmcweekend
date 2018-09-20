from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.urls import reverse 
import json
from instamojo_wrapper import Instamojo
from django.contrib import messages
from home import API_KEY,AUTH_TOKEN,EVENT_COST,ACCOMODATION_COST,ALL_EVENT_COST
import re
import requests
from django.views.decorators.csrf import csrf_exempt
from .models import Registration
from django.http import Http404
from django.conf import settings
from django.core.mail import send_mail

api = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')


# Create your views here.

def landing(request):
    return HttpResponseRedirect('/static/landing/landing.html')

def index(request):
    return render(request,'home/index.html')

def gallery(request):
    return render(request,'home/gallery.html')

def events(request):
    return render(request,'home/events.html')

def team(request):
    return render(request,'home/team.html')

    
@csrf_exempt
def register(request):
    template_name='home/register.html'
    context={
        'ecost':EVENT_COST,
        'acost':ACCOMODATION_COST,
        'offcost':ALL_EVENT_COST,
        # 'wcost':WORKSHOP_COST,
    }
    if(request.method=="POST"):
        post=request.POST
        # for i in post:
            # print(i,post[i])
        try:
            paidevents=0
            isonlinepaid=1
            dict={}
            dict['team_name']=post.get('team_name').strip()
            dict['team_leader']=post.get('team_leader').strip()
            dict['accomodation']=post.get('accomodation').strip()
            dict['contact']=post.get('contact').strip()
            dict['offline_reg']=False
            if('offline_reg' in post):
                dict['offline_reg']=True
                isonlinepaid=0
            dict['team_size']=post.get('team_size').strip()
            dict['email']=post.get('email').lower().strip()
            dict['team_size']=post.get('team_size').strip()
            dict['e_against_all_odds']=False
            dict['e_write_o_maniac']=False
            dict['e_documentary_making']=False
            dict['e_cover_art']=False
            dict['e_escapade']=False
            dict['f_3draw']=False
            dict['f_allin']=False
            dict['f_take_two']=False
            dict['f_memoravel']=False
            dict['f_selfie']=False
            dict['f_monogram']=False
            # dict['w_design']=post.get('workshop1')
            # dict['w_nikon']=post.get('workshop2')
            # dict['w_design']=int(dict['w_design'])
            # dict['w_nikon']=int(dict['w_nikon'])
            if(isonlinepaid):
                if('e_against_all_odds' in post):
                    dict['e_against_all_odds']=True
                    paidevents+=1
                if('e_write_o_maniac' in post):
                    dict['e_write_o_maniac']=True
                    paidevents+=1
                if('e_documentary_making' in post):
                    dict['e_documentary_making']=True
                    paidevents+=1
                if('e_cover_art' in post):
                    dict['e_cover_art']=True
                    paidevents+=1
                if('e_escapade' in post):
                    dict['e_escapade']=True
                    paidevents+=1
                if('f_3draw' in post):
                    dict['f_3draw']=True
                    # paidevents+=1
                if('f_allin' in post):  
                    dict['f_allin']=True
                    # paidevents+=1
                if('f_take_two' in post):
                    dict['f_take_two']=True
                    # paidevents+=1
                if('f_memoravel' in post):
                    dict['f_memoravel']=True
                    # paidevents+=1
                if('f_selfie' in post):
                    dict['f_selfie']=True
                    # paidevents+=1
                if('f_monogram' in post):
                    dict['f_monogram']=True
                # paidevents+=1
            #Validations
            if dict['team_name']=="" or dict['team_leader']=="" or dict['accomodation']=="" or dict['contact']=="" or dict['email']=="":
                messages.warning(request,"Form is not valid. You need to fill all the fields.")
                return render(request,template_name,context=context)
            
            if(not validateEmail(dict['email'])):
                messages.warning(request,"Enter a valid email address",fail_silently=True)
                return render(request,template_name,context=context)
            
            if(not dict['accomodation'].isdigit()):
                messages.warning(request,"Accomodation should be number between 0 and 5 inclusive")
                return render(request,template_name,context=context)
            
            dict['accomodation']=int(dict['accomodation'])
            
            if(not dict['team_size'].isdigit()):
                messages.warning(request,"Team size should be a number between 0 an 5 inclusive")
                return render(request,template_name,context=context)
            
            dict['team_size']=int(dict['team_size'])
            
            if(dict['accomodation']<0 or dict['accomodation']>5):
                messages.warning(request,"Accomodation should be between 0 and 5 inclusive")
                return render(request,template_name,context=context)
            
            if(dict['team_size']<1 or dict['team_size']>5):
                messages.warning(request,"Team size should be between 1 and 5 inclusive")
                return render(request,template_name,context=context)
            
            if(not re.match(r'[6-9]\d{9}',dict['contact'])):
                messages.warning(request,"Enter a valid phone number")
                return render(request,template_name,context=context)
            #amount calculation
            dict['amount_paid']=dict['accomodation']*int(ACCOMODATION_COST)*int(dict['offline_reg']) + paidevents*int(EVENT_COST)*isonlinepaid +int(dict['offline_reg'])*int(ALL_EVENT_COST)*int(dict['team_size'])
            # print("LOL")
            for i in dict:
                print(i,dict[i])
            if(dict['amount_paid']>0):
                #instamojo magic here
                response = api.payment_request_create(
                        amount=str(dict['amount_paid']),
                        purpose="FMC Weekend Team Registration",
                        send_email=False,
                        email=dict['email'],
                        buyer_name=dict['team_leader'],
                        phone=dict['contact'],
                        redirect_url=request.build_absolute_uri(reverse("checkout")),
                    )
                print(response)
                reg_obj=Registration(**dict,payment_request_id=response['payment_request']['id'])
                reg_obj.save()
                #instamojo ends here   
                return HttpResponseRedirect(response['payment_request']['longurl']) 
            else:
                reg_obj=Registration(**dict)
                reg_obj.save()
                print(reg_obj.amount_paid)
                request.session['team_id']=reg_obj.id
                print(request.session['team_id'])
                # for i in dict:
                    # print(i,dict[i])
                return HttpResponseRedirect(reverse("free_checkout"))

    
        except:
            # print("NOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
            messages.warning(request,"Fields not filled properly")
            return render(request,template_name,context=context)    
        
        
    return render(request,template_name,context=context)

def paymentConfirmationView(request):
    if(request.method=="GET"):
        try:
            payment_request_id=request.GET['payment_request_id']
            payment_id=request.GET['payment_id']
            response = api.payment_request_payment_status(payment_request_id, payment_id)
            # status=response['payment_request']['status']
            pstatus=response['payment_request']['payment']['status']
            s="<p>"+"Your Name: "+response['payment_request']['buyer_name']+"</p>"
            s+="<p>"+"Amount Paid: "+response['payment_request']['amount']+"</p>"
            s+="<p>"+"Purpose: "+response['payment_request']['purpose']+"</p>"
            s+="<p>"+"Status: "+response['payment_request']['status'] 
            # return HttpResponse(s)      
            if(pstatus=="Credit"):
                # print("HI")
                reg_obj=Registration.objects.filter(payment_request_id=str(payment_request_id))[0]
                reg_obj.payment_id=payment_id
                reg_obj.payment_status=1
                reg_obj.save()
                # print("SAVED")
                team_id=reg_obj.id
                # print(team_id)
                subject="Thanks for registration."
                subject+="<br> Your team id is "+ str(team_id)
                from_email=settings.DEFAULT_FROM_EMAIL
                to_email=str(reg_obj.email)
                # print(to_email)
                send_mail("Test Mail",subject,from_email,[to_email],fail_silently=True)
                print("YY")
            return HttpResponse(s)
        except:
            raise Http404
    raise Http404

def freeCheckoutView(request):
    try:
        team_id=request.session.get('team_id',-1)
        if(team_id==-1):
            # return(HttpResponse("HI"))
            raise Http404
        reg_obj=Registration.objects.filter(id=team_id)[0]
        p="<p>"+str(reg_obj.team_leader)+"</p>"
        return HttpResponse(reg_obj.team_leader)
    except:
        raise Http404


def validateEmail( email ):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False
