from flask import Flask,json,jsonify,Blueprint,request
from flask import current_app as app
import os
import datetime
from werkzeug import secure_filename

incident=Blueprint('incident',__name__)
incidents=[]

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
ALLOWED_EXTENSIONS = set(['png', 'jpeg', 'txt', 'gif', 'pdf', 'jpg'])


@incident.route('/',methods=['GET'])
def index():
    return jsonify({'message':"welcome"}),200

@incident.route('/api/v1/red-flags',methods=['POST'])
def postred_flags():
    if not request.headers['Content-Type']=='multipart/form-data':
          return jsonify({'msg':'request header type should be form-data'}),400
    data = request.form
    PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
    UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    image=request.files['image']
    img_name = secure_filename(image.filename)
    createfolder(app.config['UPLOAD_FOLDER'])
    saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
    image.save(saved_path)             
    incident={
          "id":len(incidents)+1,
          "created_on":datetime.datetime.utcnow(),
          "created_by":1,
          "type":data['type'],
          "location":data['location'],
          "status":'draft',
          "comment":data['comment'],
          'image':str(saved_path)


    }
    incidents.append(incident)
    return jsonify({"success":True,"incident":incident.get('id')}),201

@incident.route('/api/v1/red-flags',methods=['GET'])
def getred_flags():
        return jsonify({'data':incidents}),200

  #getting a specific red flag
@incident.route('/api/v1/red-flags/<int:id>',methods=['GET'])
def get_specific_red_flag(id):

      if not item_exists(id, incidents):
            return jsonify({'msg':'item not found'}), 404
      #find the item by id
      for incident in incidents:
            if incident['id'] == id:
                  return jsonify({'data' :incident}),200
            return jsonify({'message': 'no item found'}),404
      

#####Editing aspecific flag
@incident.route('/api/v1/red-flags/<int:id>',methods=['PUT'])
def update_specific_red_flag(id):
      if not item_exists(id,incidents):
            return jsonify({'msg':'item not found'}),404
      #CREATE A NEW LIST OBJECT
      data=request.form
            #TODO VALIDATE
      for i in incidents:
            if i['id'] == id:
                  incident={
                  "id":id,
                  "last_updated_on":datetime.datetime.utcnow(),
                  "created_by":1,
                  "type":data['type'],
                  "location":data['location'],
                  "status":"draft",
                  "comment":data['comment']
             }
            i.update(incident)
                
      return jsonify({"msg":"updated"}),200

@incident.route('/api/v1/red-flags/<int:id>',methods=['DELETE'])
def delete_red_flags(id):
    #find the item by id
    if not item_exists(id,incidents):
       return jsonify({'msg':'item not found'}),404

    for incident in incidents:
        if incident['id']==id:
           incidents.remove(incident)
    return jsonify({'Message': "item deleted"}),200
    

def item_exists(item_id,itemlist):
      for item in itemlist:
            if item['id']==item_id:
                  return True
      return False


def createfolder(local_dir):
      newpath=local_dir
      if not os.path.exists(newpath):
            os.makedirs(newpath)
      return newpath