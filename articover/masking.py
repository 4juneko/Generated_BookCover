"""Interfaces for text detection."""
from articover.text_detector import TextBox
from PIL import Image, ImageDraw
from typing import Sequence

class MaskGenerator:
    def __init__(self):
        pass

    
    def selected_masks(self, text_boxes: Sequence[TextBox], height: int, width: int, mode: str, selected_box_indices):
        num_channels = len(mode)
        background_color = tuple([0] * num_channels)
        mask_color = tuple([255] * num_channels)
        
        selected_masks = []
        masks = []

        inpainting_mask = Image.new(mode, (width, height), background_color)
        inpainting_mask_draw = ImageDraw.Draw(inpainting_mask)
        
        for i, text_box in enumerate(text_boxes, start=1):
            mask = Image.new(mode, (width, height), background_color)
            draw = ImageDraw.Draw(mask)
            draw.rectangle(xy=(text_box.x, text_box.y, text_box.x + text_box.w, text_box.y - text_box.h),
                           fill=mask_color)

            if i in selected_box_indices:
                selected_masks.append(mask)
            else:
                inpainting_mask_draw.rectangle(xy=(text_box.x, text_box.y, text_box.x + text_box.w, text_box.y - text_box.h),
                                fill=mask_color)
        
        return inpainting_mask, selected_masks


    def generate_mask(self, text_boxes: Sequence[TextBox], in_image_path: str, selected_box_indices):##
        image = Image.open(in_image_path)
        inpainting_mask, selected_masks = self.selected_masks(text_boxes, image.height, image.width, image.mode, selected_box_indices)
        return inpainting_mask, selected_masks

