import json
from flask import jsonify,request
from flask_httpauth import HTTPBasicAuth
from pkg.api import apiobj
from pkg.models import db

auth=HTTPBasicAuth()


# @auth.get_password
# def get_password(username):
#     '''This function will recive username and fetch the respective password'''
#     deets= User.query.filter(User.user_email==username).first()
#     if deets:
#         return deets.user_password
#     else:
#         return None

@auth.error_handler
def unauthorized():
    data2send={"status":False, "msg":"invalid Access", "data":[]}
    return jsonify(data2send), 401


@apiobj.get('/')
def home():
    return '<h2>Page of API</h2>'

# @apiobj.post('/add/')
# @auth.login_required
# def add_chef():
#     #{"fullname":"Hilda Bacci", "bio":"A guiness world record","pix":"http://127.0.0.1:8087/static/pic/lekkiapt3.jpg"}
#     if request.is_json:
#        data_received= request.get_json()
#        chefname = data_received.get('fullname') #data_received['fullname']
#        chefbio = data_received.get('bio') #data_received['fullname']
#        chefpix = data_received.get('pix') #data_received['fullname']
#        if chefname !=None and chefbio !=None and chefpix!=None:   
#         c=Chef(chef_fullname=chefname,chef_bio=chefbio,chef_profilepix=chefpix)
#         db.session.add(c)
#         db.session.commit()
#         cid=c.chef_id
#         data2send={"status":True,"msg":f"A new chef with id {cid} has been added","data":[]}
#         return jsonify(data2send),200
#         # return f'A new chef with id {cid} has been created'
#        else:
#            data2send={"status":False,"msg":"one or more fields is missing", "data":[]}
#            return jsonify(data2send),400
#     else:
#         data2send={"status":False,"msg":"Bad Request Format", "data":[]}
#         return jsonify(data2send),400
    

@apiobj.app_errorhandler(405)
def bad_method(error):
    data2send={"status":False,"msg":"Method Not Allowed", "data":[]}
    return jsonify(data2send),405

@apiobj.app_errorhandler(404)
def not_found(error):
    data2send={"status":False,"msg":"Page not found", "data":[]}
    return jsonify(data2send),404


    

# @apiobj.get('/chef/all/')
# def list_all():
#     deets = db.session.query(Chef).all()
#     data=[]
#     for d in deets: # we are looping over every object and generating dictionary from it, at the end of it append to a list so jsonify can be a list of dictionary
#         single = dict()
#         single['fullname'] = d.chef_fullname
#         single['bio'] = d.chef_bio
#         single['pix'] = d.chef_profilepix
#         data.append(single)
        


    data2send={"status":True,"msg":f"A new chef with id has been added","data":data} #work on this
    return jsonify(data2send)


# converting to json 
# @apiobj.get('/chef/<id>/')
# def get_chef(id):
#     deets=Chef.query.get(id) #<Chef1>
#     data=dict()
#     if deets:
#         data['fullname']=deets.chef_fullname
#         data['bio']=deets.chef_bio
#         data['pix']=deets.chef_profilepix
#         data2send={"status":True,"msg":"view Chef details","data":data}
#         return jsonify(data2send),200
#     else:
#         data2send={"status":False,"msg":"Invalid details","data":data}
#         return jsonify(data2send),400


        
    #return json.dumps(data) #dumps helps conver from py dict to json
    