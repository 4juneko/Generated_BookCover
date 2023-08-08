"""Interfaces for text detection."""
from dataclasses import dataclass
from typing import Sequence

#keras-ocr detecting
import numpy as np

from . import detecting, tools


class MaskGenerator:
    def __init__(self):
        pass

    def _make_mask(self, text_boxes: Sequence[TextBox], height: int, width: int, mode: str, out_mask_dir) -> Image:
        """Returns a black image with white rectangles where the text boxes are."""
        num_channels = len(mode)
        background_color = tuple([0] * num_channels)
        mask_color = tuple([255] * num_channels)

        final_mask = Image.new(mode, (width, height), background_color)
        final_mask_draw = ImageDraw.Draw(final_mask)
   
        for i, text_box in enumerate(text_boxes, start=1):
            #mask images for each text box
            mask = Image.new(mode, (width, height), background_color)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.rectangle(xy=(text_box.x, text_box.y, text_box.x + text_box.w, text_box.y - text_box.h),
                                fill=mask_color)
            mask_filename = f'mask{i}.png'
            full_mask_path = os.path.join(out_mask_dir, mask_filename)
            mask.save(full_mask_path)

            #a mask image of text boxes
            final_mask_draw.rectangle(xy=(text_box.x, text_box.y, text_box.x + text_box.w, text_box.y - text_box.h),
                                fill=mask_color)
            
        return final_mask

    def generate_mask(self, text_boxes: Sequence[TextBox], in_image_path: str, out_mask_dir):##
        image = Image.open(in_image_path)
        final_mask_image = self._make_mask(text_boxes, image.height, image.width, image.mode, out_mask_dir)
        return final_mask_image

