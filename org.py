from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import uuid
import torch
import numpy as np

class StableDiffusion():
    def __init__(self, img_size=768, num_inference_steps=50, num_images_per_prompt=1, device = None):
        if device is None:
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.img_size = img_size
        self.num_inference_steps = num_inference_steps
        self.num_images_per_prompt = num_images_per_prompt
        print("img_size", img_size)
        print("num_inference_steps", num_inference_steps)
        print("num_images_per_propmt", num_images_per_prompt)
        
        model_id = "stabilityai/stable-diffusion-2-1"   
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id, 
            torch_dtype=torch.float16 
        )
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        pipe.enable_attention_slicing()
        self.pipe = pipe.to(device)
        print('init')

    def predict(self, prompt, cb = None) -> np.ndarray:
        result = self.pipe(prompt,
                    callback=cb,
                    width=self.img_size,
                    height=self.img_size,
                    num_inference_steps=self.num_inference_steps,
                    num_images_per_prompt=self.num_images_per_prompt,
                    output_type='str'
                    )
        return result.images
            
    def image(self, prompt, cb = None) -> None:
        result = self.pipe(prompt,
                            callback=cb,
                            width=self.img_size,
                            height=self.img_size,
                            num_inference_steps=self.num_inference_steps,
                            num_images_per_prompt=self.num_images_per_prompt,
                            output_type='pil'
                        )
        for img in result.images:
            fname = "./outputs/output_{}.png".format(uuid.uuid4())
            print("save as ", fname)
            img.save(fname)

def cb(step, a, b):
    print('a;', step)


if __name__ == '__main__':
    # prompt = "brain, cartoon style, concept art, pop, cute"
    prompt = "charming white cat::drawing cartoon::pop style::concept art"
    # s = StableDiffusion(img_size=512, num_inference_steps=75)
    s = StableDiffusion(num_inference_steps=100)
    # s.predict(prompt, cb)
    s.image(prompt)
