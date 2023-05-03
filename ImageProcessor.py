import numpy as np
import cv2
import logging

logging.basicConfig(filename='image_processor.log', level=logging.INFO)

class ImageProcessor:
    def __init__(self):
        self.image = None
        self.ft = None

    def open_image(self, file_obj) -> bool:
        self.image = cv2.imdecode(np.frombuffer(file_obj.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
        if self.image is None:
            logging.error(f"Failed to open image")
            return False
        self.ft = np.fft.fft2(self.image)
        logging.info(f"Opened image")
        return True

    def check_size(self, other_image: np.ndarray) -> bool:
        if self.image.shape == other_image.shape:
            return True
        logging.warning("Image sizes do not match")
        return False

    def display_image(self, component: str) -> np.ndarray:
        if component == "magnitude":
            return np.log(np.abs(self.ft) + 1)
        elif component == "phase":
            return np.angle(self.ft)
        elif component == "real":
            return self.ft.real
        elif component == "imaginary":
            return self.ft.imag
        elif component == "uniform_magnitude":
            return np.ones_like(self.ft)
        elif component == "uniform_phase":
            return np.zeros_like(self.ft)
        else:
            logging.warning(f"Invalid component: {component}")
            return None

    def mix_components(self, other_image: np.ndarray, component1: str, component2: str, ratio: float) -> np.ndarray:
        if component1 == "magnitude":
            ft1 = np.abs(self.ft)
        elif component1 == "phase":
            ft1 = np.exp(1j * np.angle(self.ft))
        elif component1 == "real":
            ft1 = self.ft.real
        elif component1 == "imaginary":
            ft1 = self.ft.imag
        elif component1 == "uniform_magnitude":
            ft1 = np.ones_like(self.ft)
        elif component1 == "uniform_phase":
            ft1 = np.zeros_like(self.ft)
        else:
            logging.warning(f"Invalid component: {component1}")
            return None

        if component2 == "magnitude":
            ft2 = np.abs(np.fft.fft2(other_image))
        elif component2 == "phase":
            ft2 = np.exp(1j * np.angle(np.fft.fft2(other_image)))
        elif component2 == "real":
            ft2 = np.fft.fft2(other_image).real
        elif component2 == "imaginary":
            ft2 = np.fft.fft2(other_image).imag
        elif component2 == "uniform_magnitude":
            ft2 = np.ones_like(self.ft)
        elif component2 == "uniform_phase":
            ft2 = np.zeros_like(self.ft)
        else:
            logging.warning(f"Invalid component: {component2}")
            return None

        mixed_ft = (1 - ratio / 100) * ft1 + (ratio / 100) * ft2
        mixed_image = np.fft.ifft2(mixed_ft).real
        mixed_image = cv2.normalize(mixed_image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        return mixed_image
