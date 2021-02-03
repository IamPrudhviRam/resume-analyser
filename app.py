from flask import Flask
from flasgger import Swagger
from flask import request
import demo.categorise_ranking as categorise_ranking
import demo.dl_based_parser_predict as predict

app=Flask(__name__)
Swagger(app)

@app.route('/')
def hello():
    return '<h2> Api Working for Resume</h2><h4> "/predict" for predicting</h4>' \
           '<h4> "/ranking" for Ranking</h4>' \
           '<h4> "/confusion" for confusion matrix and accuracy</h4>'

@app.route('/predict')
def main():
    new_data=predict.main()
    return '<h2>Files Predicted</h2><p>{new_data}</p>'.format(new_data=new_data)


@app.route('/ranking', methods=['POST'])
def ranking():
    jd = request.form['jd']
    categorised_dict= categorise_ranking.get_cr_values(nlp(jd))
    return'<h2>Resume Ranking done.</h2><p>Categorized Candidates :\n {rank} < / p > '.format(rank=categorised_dict)
	
if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080)