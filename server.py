from flask import Flask,jsonify,request
from flask_cors import CORS
from path_finder import get_paths,getCustomers,getTargets,getAll

app = Flask(__name__)
CORS(app)

@app.route('/',methods=['GET','POST'])
def index():
    source,target,leaf=str(request.data).split(',')
    return jsonify(get_paths(source,[],[],target,0,[],leaf))

@app.route('/customers',methods=['GET'])
def getCust():
    return jsonify(getCustomers([]))

@app.route('/targets',methods=['POST'])
def getTarg():
    option,source=str(request.data).split(',')
    return jsonify(getTargets([],option,source))

@app.route('/all',methods=['GET'])
def getAllNodes():
    return jsonify(getAll([]))

if __name__ == '__main__':
    app.run(debug=True,threaded=True,port=5000)
