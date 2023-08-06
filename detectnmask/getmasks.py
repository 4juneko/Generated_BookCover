from detectnmask.text_detector import Keras_OCR
from detectnmask.masking import MaskGenerator

class get_masks:
    def __init__(self, detector = None, masker = None):
        self.detector = detector() if detector else Keras_OCR()
        self.masker = masker() if masker else MaskGenerator()
    def masks(self, in_image_path: str, out_mask_dir: str):
        print(f"\tCalling text detector...")
        text_boxes = self.detector.detect_text(in_image_path)
        print(f"\tDetected {len(text_boxes)} text boxes.")

        if not text_boxes:
            print('Detected 0 text_boxes. No masks will be made.')
        else:
            print(f"\tCalling masking model...")

            import os
            assert os.path.exists(out_mask_dir)
            
            final_mask=self.masker.generate_mask(text_boxes, in_image_path, out_mask_dir)

            fmfilename = 'finalmask.png'
            full_mask_path = os.path.join(out_mask_dir, fmfilename)
            final_mask.save(full_mask_path)