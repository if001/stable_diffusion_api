# readme
stable diffusion test

## rinna.py
日本語版 stable diffusion

## org.py
stable-diffusion-2-1


## server.py
python server.py

```
optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT
  --host HOST
  -v, --verbose
  --prod
  -s NUM_INFERENCE_STEPS, --num_inference_steps NUM_INFERENCE_STEPS
  -n NUM_IMAGES_PER_PROMPT, --num_images_per_prompt NUM_IMAGES_PER_PROMPT
  --use_dummy           use dummy stable diffusion
  --device DEVICE       torch run device. default cpu
```


### client

```
$curl -X GET 'localhost:5000/predict?prompt=cute,brain'

{
  "image": "",
  "message": "ok"
}
```

or

`sh req.sh`

