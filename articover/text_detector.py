from dataclasses import dataclass
from typing import Sequence

import numpy as np
from articover import detecting, tools


@dataclass
class TextBox:
  # (x, y) is the top left corner of a rectangle; the origin of the coordinate system is the top-left of the image.
  # x denotes the vertical axis, y denotes the horizontal axis (to match the traditional indexing in a matrix).
  x: int
  y: int
  h: int
  w: int
  A: int

class Keras_OCR:
    """Uses the 'Keras-OCR' to do text detection."""
    def __init__(self, detector=None, scale=2, max_size=2048):
        if detector is None:
            detector = detecting.Detector()
        self.scale = scale
        self.detector = detector
        self.max_size = max_size

    def detect_text(self, image_filename: str, detection_kwargs=None) -> Sequence[TextBox]:
        """Run the text detection on an image.

        Args:
            image_filename: The image to parse
            detection_kwargs: Arguments to pass to the detector call

        Returns:
            A list of lists of TextBox instances.
        """
        image = image_filename
        
        # Make sure we have an image array to start with.
        if not isinstance(image, np.ndarray):
            image = tools.read(image)

        # This turns an image into (image, scale) tuples temporarily
        image, scale = tools.resize_image(image, max_scale=self.scale, max_size=self.max_size)
        
        max_height, max_width = image.shape[:2]
        images = tools.pad(image, width=max_width, height=max_height)

        if detection_kwargs is None:
            detection_kwargs = {}

        box_groups = self.detector.detect(images=images[np.newaxis, ...], **detection_kwargs)
        
        box_groups = [
            tools.adjust_boxes(boxes=boxes, boxes_format="boxes", scale=1 / scale)
            if scale != 1
            else boxes
            for boxes in box_groups
        ]
        text_boxes = []
        for boxes in box_groups:
            x = boxes[3][0]
            y = boxes[3][1]
            h = boxes[3][1]-boxes[0][1]
            w = boxes[2][0]-boxes[3][0]
            A = w*h
            text_boxes.append(TextBox(int(x),int(y),int(h),int(w),int(A)))

        return text_boxes

