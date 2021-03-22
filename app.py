import json

from flask import Flask, jsonify
from flasgger import Swagger
from flask import request
from werkzeug.utils import secure_filename
import shutil
import demo.categorise_ranking as categorise_ranking
from pyngrok import ngrok
import os
import demo.dl_based_parser_predict as predict

app=Flask(__name__)
Swagger(app)
public_url = ngrok.connect(5000).public_url
print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, 5000))

@app.route('/')
def hello():
    return '<h2> Api Working for Resume</h2><h4> "/predict" for predicting</h4>' \
           '<h4> "/ranking" for Ranking</h4>' \
           '<h4> "/confusion" for confusion matrix and accuracy</h4>'

@app.route('/predict')
def main():
    new_data=predict.main()
    #return '<h2>Files Predicted</h2><p>{new_data}</p>'.format(new_data=new_data)
    return jsonify({'result': 'files added successfully'})


@app.route('/ranking', methods=['POST'])
def ranking():
    jd = request.form['jd']
    categorised_dict= categorise_ranking.get_cr_values(jd)
    return jsonify(categorised_dict)
    #return'<h2>Resume Ranking done.</h2><p>Categorized Candidates :\n {rank} < / p > '.format(rank=categorised_dict)



@app.route('/resumes', methods=['POST'])
def resumevalues():
   # file = request.files['resumes']
   dir_path = 'instance'
   try:
       shutil.rmtree(dir_path)
   except OSError as e:
       print("Error: %s : %s" % (dir_path, e.strerror))
   # create the folders when setting up your app
   os.makedirs(os.path.join(app.instance_path, 'TestingData'), exist_ok=True)
   for f in request.files.getlist('resumes'):  # myfile is the name of your html file button
        filename = f.filename
        print(" ffffilename ",filename)
        # when saving the file
        f.save(os.path.join(app.instance_path, 'TestingData', secure_filename(filename)))
   return jsonify({'result': 'files added successfully'})



if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080)