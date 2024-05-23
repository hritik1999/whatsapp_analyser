from flask import Flask,request,jsonify
from flask_cors import CORS
from uagents.query import query
from application.models import Message
import json

chunker_address = 'agent1q05pvyy4c5sraah8tck40urrpmnwh3dt5p6fa9znr9cj960cnka7v9n00d2'
analyser_address = 'agent1qtladakw5ly6ap6xk4azz7p4r995rwjr3x8xm2yer479qdf502hvur2wpa4'

def create_app():
    app = Flask(__name__)
    CORS(app,resources={r"/*": {"origins": "*"}})
    return app

app = create_app()

@app.route('/analyse_chat', methods=['POST']) 
async def index():
    file = request.files['file'].read().decode('utf-8')
    text_chunks = await query(destination=chunker_address,message=Message(message=file))
    text_chunks = json.loads(text_chunks.decode_payload())['message']
    analysis = await query(destination=analyser_address,message=Message(message=text_chunks),timeout=1000)
    analysis = json.loads(analysis.decode_payload())['message']
    return jsonify(json.loads(analysis))

if __name__ == '__main__':
    app.run(debug=True)