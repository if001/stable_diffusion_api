# readme
stable diffusion test

## rinna.py
日本語版 stable diffusion

## org.py
use stable-diffusion-2-1

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

### params

GET `/echo`
params:
return:

GET `/predict`
params: `prompt=[str]`
return: image array


POST `/make_image`
for slack slash command

### set env value
SLACK_TOKEN: bot user token.
CHANNEL: file send channel id. default send to local_sch(stable_diffusion channel)

ローカルで動かす場合は、`.env`を追加。

```
SLACK_TOKEN=token
CHANNEL=channel
```

##  client

```bash
$curl -X GET 'localhost:5000/predict?prompt=cute,brain'

{
  "image": "",
  "message": "ok"
}
```

or

`sh req.sh`

## slack
サーバーでは、slackのslach commandを受け取って、slackにメッセージを送る

slackでappを作り、channel_idとtokenを取ってくる

file sendの詳細はここを参照

https://api.slack.com/methods/files.upload
