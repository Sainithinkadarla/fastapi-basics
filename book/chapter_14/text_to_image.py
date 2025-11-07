from PIL import Image
from typing import Callable
from diffusers import StableDiffusionPipeline
import torch

class Text2Image:
    pipe: StableDiffusionPipeline | None = None
    def load_model(self):
        if torch.cuda.is_available():
            device = "cuda"
        elif torch.backends.mps.is_available():
            device = "mpu"
        else:
            device = "cpu"

        pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
        pipe.to(device)
        self.pipe = pipe

    def generate(self, prompt: str, *, negative_prompt: str | None = None, 
                 steps: int = 50, callback: Callable[[int, int, torch.FloatTensor], None] | None = None) -> Image.Image:  
        if not self.pipe:
            raise RuntimeError("Model is not loaded")
        return self.pipe(prompt, negative_prompt = negative_prompt, 
                         num_inference_steps=steps, 
                         callback= callback,
                         callback_steps = 10,
                         guidance_scale = 0.9).images[0]
    
if __name__ == "__main__":
    text_to_image = Text2Image()
    text_to_image.load_model()

    def callback(step: int, _timestep, _tensor):
        print(f"👉 step {step}")

    image = text_to_image.generate("A beautiful place with pond", 
                                   negative_prompt="low quality, ugly", 
                                   callback=callback)

    image.save("output.png")