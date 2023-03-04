import torch
from torch import autocast
from diffusers import LMSDiscreteScheduler
from japanese_stable_diffusion import JapaneseStableDiffusionPipeline
import uuid


# model_id = "rinna/japanese-stable-diffusion"
model_id = "./model"
device = "cuda"
# Use the K-LMS scheduler here instead
# scheduler = LMSDiscreteScheduler(beta_start=0.00085, beta_end=0.012, beta_schedule="scaled_linear", num_train_timesteps=1000)
scheduler = LMSDiscreteScheduler(beta_start=0.00085, beta_end=0.012, beta_schedule="scaled_linear", num_train_timesteps=1000)

pipe = JapaneseStableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, use_auth_token=True, torch_dtype=torch.float16)
# pipe = JapaneseStableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, use_auth_token=True, torch_dtype=torch.float16)
# pipe.save_pretrained('./model')

pipe = pipe.to(device)

prompt = "間抜けで可愛らしい白い猫 漫画風"
with autocast("cuda"):
    # result = pipe(prompt, guidance_scale=7.5)
    result = pipe(prompt, guidance_scale=10.0, num_images_per_prompt=1)
    print(result)
    image = result.images[0]
    # image = pipe(prompt, guidance_scale=7.5)["sample"][0]

image.save("./outputs/output_{}.png".format(uuid.uuid4()))