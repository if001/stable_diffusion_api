from org import StableDiffusion
from flask import Flask,request, jsonify
# from flask_socketio import SocketIO, send, emit
import argparse
from waitress import serve
import logging
import io

from send_slack import send_file

app = Flask(__name__)

class Dummy():
    def __init__(self) -> None:    
        app.logger.info('use dummy')
        name = "dummy"

    def predict(self, prompt):
        return 'dummy'
        
class InitModelMiddlewere:
    def __init__(self, app, stableDiffusion):
        self.app = app
        self.sd = stableDiffusion        

    def __call__(self, environ, start_response):    
        if 'sd' not in environ.keys():                    
            environ['sd'] = self.sd
        return self.app(environ, start_response)

def img_to_byte(img):
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format='png')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

@app.before_request
def log_request_info():
    app.logger.info('%s - %s - %s - %s', request.remote_addr, request.method, request.url, request.query_string)

@app.route("/", methods=['GET'])
def echo():
    return {
        "message": 'ok',
    }

"""
query_string(required): prompt
return: image array
"""
@app.route('/predict', methods=['GET'])
def predict():
    args = request.args    
    prompt = args.get('prompt')
    if prompt is None:
        return jsonify({'message': 'prompt must set'}), 400

    if 'sd' not in request.environ.keys():
        return jsonify({'message': 'sd not set...'}), 500
    
    sd = request.environ['sd']

    try: 
        sd = request.environ['sd']
        result = sd.predict(prompt)
        images = [ v.tolist() for v in result]
        return jsonify({ 'message': 'ok', 'images': images })
    except Exception as e:
        app.logger.info('exception %s', e)
        return jsonify({'message': 'server error'}), 500

@app.route('/post_json', methods=['POST'])
def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        return json
    else:
        return 'Content-Type not supported!'
    
"""
for slack slash command
"""
@app.route('/make_image', methods=['POST'])
def make_image(): 
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        return jsonify({'message': 'set content_type json'}), 400

    prompt = request.json['text']
    if prompt is None:
        return jsonify({'message': 'prompt must set'}), 400
    
    if 'sd' not in request.environ.keys():
        return jsonify({'message': 'sd not set...'}), 500
    sd = request.environ['sd']

    try: 
        sd = request.environ['sd']        
        predict_images = sd.predict(prompt)
        if predict_images == "dummy":
            return jsonify({ 'message': 'ok, use dummy' })        
        for img in predict_images:
          b = img_to_byte(img)
          msg = "crate prompt is {}".format(prompt)
          r = send_file(msg, b)
          app.logger.info('send slack result: %s', r)
        return jsonify({ 'message': 'ok' })
    except Exception as e:
        app.logger.info('exception %s', e)
        return jsonify({'message': 'server error'}), 500

def run(host, port, isDev):    
    app.logger.info('run.. {}:{}'.format(host, port))
    if isDev:
        # app.run(host, port, debug=args.verbose)
        app.run(host, port, debug=True)        
    else:    
        app.logger.info('run as prod')
        serve(app, host=host, port=port, threads=10, url_scheme='http')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=5000)
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('--dev', action='store_true')

    parser.add_argument('-s', '--num_inference_steps', default=50, type=int)
    parser.add_argument('-n', '--num_images_per_prompt', default=1, type=int)
    parser.add_argument('--use_dummy', action='store_true', help='use dummy stable diffusion')
    parser.add_argument('--device', default=None, help='torch run device. default cpu')

    args = parser.parse_args()

    if args.use_dummy:
        sd = Dummy()
    else:        
        img_size=768
        sd = StableDiffusion(img_size=64,
                            num_inference_steps = args.num_inference_steps, 
                            num_images_per_prompt= args.num_images_per_prompt
                            )    
    app.wsgi_app = InitModelMiddlewere(app.wsgi_app, sd)    
    app.logger.setLevel(logging.INFO)
    run(args.host, args.port, args.dev)
    # socketio.run(app, debug=True)