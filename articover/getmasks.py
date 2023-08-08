from articover.text_detector import Keras_OCR
from articover.masking import MaskGenerator
from articover import tools
import numpy as np


class get_masks:
    def __init__(self, detector = None, masker = None):
        self.detector = detector() if detector else Keras_OCR()
        self.masker = masker() if masker else MaskGenerator()
    def masks(self, in_image_path: str, selected_box_indices):
        print(f"\tCalling text detector...")
        text_boxes = self.detector.detect_text(in_image_path)
        print(f"\tDetected {len(text_boxes)} text boxes.")

        image=in_image_path
        if not isinstance(image, np.ndarray):
            image = tools.read(image)
            
        if not text_boxes:
            print('Detected 0 text_boxes. No masks will be made.')
        else:
            print(f"\tCalling annotating model...")
            annot_image =tools.drawAnnotations(image, text_boxes)
            
            print(f"\tCalling masking model...")
            
            inpainting_mask, selected_masks=self.masker.generate_mask(text_boxes, in_image_path, selected_box_indices)
            
            print("Done.")

            return inpainting_mask, selected_masks, annot_image