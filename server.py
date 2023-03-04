from org import StableDiffusion
from flask import Flask,request, jsonify
# from flask_socketio import SocketIO, send, emit
import argparse
from waitress import serve

app = Flask(__name__)

class Dummy():
    def __init__(self) -> None:
        print('use dummy...')

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

@app.route("/", methods=['GET'])
def echo():
    return {
        "message": 'ok',
    }

@app.route('/predict', methods=['GET'])
def predict():
    args = request.args    
    prompt = args.get('prompt')
    if prompt is None:
        return jsonify({'message': 'prompt must set'}), 400

    if 'sd' not in request.environ.keys():
        return jsonify({'message': 'sd not set...'}), 500
    
    try: 
        sd = request.environ['sd']
        result = sd.predict(prompt)
        images = [ v.tolist() for v in result]
        return jsonify({ 'message': 'ok', 'images': images })
    except Exception as e:
        print('exception ', e)
        return jsonify({'message': 'server error'}), 500

# ## websocket
# socketio = SocketIO(app, cors_allowed_origins='*')

# @socketio.on('connect')
# def connect(auth):
#     pass

# @socketio.on('disconnect')
# def disconnect():
#     pass

# @socketio.on('request')
# def handle_generate_request(json):
#     pass

# @socketio.on('result')
# def handle_generate_response(json):
#     pass


def run(host, port, isProd):
    if isProd:
        serve(app, host=host, port=port, threads=10, url_scheme='http')
    else:
        # app.run(host, port, debug=args.verbose)
        app.run(host, port, debug=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=5000)
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('--prod', action='store_true')

    parser.add_argument('-s', '--num_inference_steps', default=50)
    parser.add_argument('-n', '--num_images_per_prompt', default=1)
    parser.add_argument('--use_dummy', action='store_true', help='use dummy stable diffusion')
    parser.add_argument('--device', default=None, help='torch run device. default cpu')

    args = parser.parse_args()    
    if args.use_dummy:
        sd = Dummy()
    else:        
        sd = StableDiffusion(img_size=768,
                            num_inference_steps = args.num_inference_steps, 
                            num_images_per_prompt= args.num_images_per_prompt
                            )    
    app.wsgi_app = InitModelMiddlewere(app.wsgi_app, sd)
    run(args.host, args.port, args.prod)
    # socketio.run(app, debug=True)