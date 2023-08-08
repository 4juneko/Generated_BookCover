import cv2
import numpy as np
from PIL import Image
from articover.text_detector import Keras_OCR
from articover.masking import MaskGenerator
from articover import tools
from huggingface_hub import notebook_login
import inspect
from typing import List, Optional, Union

import numpy as np
import torch
import PIL
import gradio as gr
from diffusers import StableDiffusionInpaintPipeline
from articover.text_detector import Keras_OCR
from articover.masking import MaskGenerator
from articover import tools
import matplotlib.pyplot as plt


def detect_annotate(in_image_path):
    detector = Keras_OCR()
    text_boxes = detector.detect_text(in_image_path)
    image = in_image_path
    if not isinstance(image, np.ndarray):
        image = tools.read(image)
    if not text_boxes:
        pass
    else:
        annot_image =tools.drawAnnotations(image, text_boxes)
        return text_boxes, annot_image
    

def mask_inpainting_STE(text_boxes, in_image_path, text_box_num: list, words: list) -> Image.Image:
    #mask
    masker = MaskGenerator()
    inpainting_mask, selected_masks=masker.generate_mask(text_boxes, in_image_path, text_box_num)
    
    #inpaint
    image = PIL.Image.open(in_image_path).resize((512, 512))
    mask_image = PIL.Image.open(inpainting_mask).resize((512, 512))
    
    
    device = "cuda"
    model_path = "runwayml/stable-diffusion-inpainting"

    pipe = StableDiffusionInpaintPipeline.from_pretrained(
        model_path,
        torch_dtype=torch.float16,
    ).to(device)
    
    prompt = "plain background"
    
    guidance_scale=7.5
    num_samples = 1
    generator = torch.Generator(device="cuda").manual_seed(0) # change the seed to get different results
    
    inpainted_image = pipe(
        prompt=prompt,
        image=image,
        mask_image=mask_image,
        guidance_scale=guidance_scale,
        generator=generator,
        num_images_per_prompt=num_samples,
    ).images[0]

    inpainted_image.save("examples/mask7.png")
    
    #STE
    model_path = "/path/to/model"
    input_image = "examples/mask7.png"
    
    for _ in range(3):
        for i in text_box_num:
            mask = selected_masks[i]
            resized_mask = mask.resize((256,256), Image.ANTIALIAS)
            resized_mask.save(f"examples/mask{7+i}.png")  
            input_mask = f"examples/mask{7+i}.png"
            text = words[i]
            output_filename=f"output{i+1}"
            output_dir = "/path/to/output"
            command = f"python generate.py --ckpt_path {model_path} --in_image {input_image} --in_mask {input_mask} --text {text} --output_dir {output_dir} --num_sample_per_image 1"
            !{command}
                        
            output_image_path = os.path.join(opt.out_dir, output_filename)
    #원하면 PIL.Image.Image 객체 return하면 된다.

    