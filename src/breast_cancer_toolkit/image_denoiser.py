import cv2
import numpy as np

from skimage.morphology import disk

class Denoiser:
    def __call__(self, image):
        return self.denoise(image)

    def denoise(self, image):
        pass


class ClassicDenoiser(Denoiser):
    def denoise(self, img):
        """
          In the first step, we used the threshold value 200 (?) to generate a binary mask,
          where 0 (black) and 1 (white) is the background pixel, and s the breast region, artifact,
          or noise pixel.
        """
        _, binary_mask = cv2.threshold(img, 67, 255, cv2.THRESH_BINARY)

        """A morphological opening operator is applied to the binary image with a disk-type structuring element of 
        size 9 × 9 to extract the breast tissue area; it is more prominent than any object; it is binarized as a 
        single region. Then, we overlay this mask to eliminate mammography artifacts and keep only the breast tissue 
        area."""
        opened_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_OPEN, disk(9))
        masked_image = cv2.bitwise_and(img, img, mask=opened_mask)

        # We need some semantic segmentation
        # The code below removes the borders
        # masked_image = masked_image[50:masked_image.shape[0],:]

        """
           The bounding box of the breast tissue is used to crop each view so that it mainly contains the breast tissue.
        """
        contours, _ = cv2.findContours(masked_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        largest_contour = max(contours, key=cv2.contourArea)
        contour_image = np.zeros_like(img)
        cv2.drawContours(contour_image, [largest_contour], -1, (255, 255, 255), thickness=cv2.FILLED)
        contour_image = cv2.bitwise_and(masked_image, contour_image)

        """
           Furthermore, we use magma color mapping from 16-bit grayscale to 24-bit RGB,
        """
        false_colored_img = cv2.applyColorMap(contour_image, cv2.COLORMAP_MAGMA)

        return cv2.resize(false_colored_img, (224, 336))
