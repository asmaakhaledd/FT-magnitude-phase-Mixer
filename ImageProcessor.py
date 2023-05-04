import numpy as np
import cv2
import logging

logging.basicConfig(filename='image_processor.log', level=logging.INFO)

class ImageProcessor:
    def __init__(self):
        self.image = None 
        self.ft = None
        self.ft_shift=None

    def perform_fft(self):
        self.ft = np.fft.fft2(self.image)
        self.ft_shift = np.fft.fftshift(self.ft)    

    def open_image(self, file) -> bool:
        self.image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
        if self.image is None:
            logging.error(f"Failed to open image")
            return False
        logging.info(f"Opened image")
        return True

    def display_image(self, component):
        result=0
        if component == "Magnitude":
            #absolute value of the complex number at each point in the Fourier transformed image. It represents the strength of the corresponding frequency component. 
            #By taking the logarithm of the magnitude, we can obtain a more visually interpretable version of the Fourier spectrum (magnitude spectrum)
            result = np.log(np.abs(self.ft_shift))
        elif component == "Phase":
            #angle of the complex number at each point in the Fourier transformed image. It represents the position of the corresponding frequency component in the image.
            result =  np.angle(self.ft_shift)
        elif component == "Real":
            result =  np.real(self.ft_shift)
        elif component == "Imaginary":
            result =  np.imag(self.ft_shift)
        elif component == "Uniform Magnitude":
            magnitude = np.abs(self.ft_shift)
            uniform_magnitude = np.ones_like(magnitude) * np.mean(magnitude)
            #By taking the logarithm of the magnitude, we can obtain a more visually interpretable version of the Fourier spectrum (magnitude spectrum)
            result = np.log(magnitude / uniform_magnitude)
        elif component == "Uniform Phase":
            #Uniform phase refers to a transformation applied to the phase spectrum of an image such that all the phase values become uniformly distributed across the spectrum. This is done to remove any abrupt changes in the phase of the image, which can cause artifacts or distortions in the reconstructed image.
            phase =  np.angle(self.ft_shift)
            #calculate the uniform phase spectrum by taking the exponential of the angle of the Fourier transform coefficients to create a phase spectrum with a more uniform distribution of values
            uniform_phase = np.exp(1j * phase)
            # create a new Fourier transform with a more uniform phase spectrum
            new_ft_shift=self.ft_shift * uniform_phase
            #get the angle/phase of the uniform phase new ft
            result = np.angle(new_ft_shift)
        else:
            logging.warning(f"Invalid component: {component}")
            return None
        norm = cv2.normalize(result, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        retval, buffer = cv2.imencode('.jpg', norm)
        response = buffer.tobytes()
        logging.info(f"Applied transformation on image")
        return response


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


    # def check_size(self, other_image: np.ndarray) -> bool:
    #     if self.image.shape == other_image.shape:
    #         return True
    #     logging.warning("Image sizes do not match")
    #     return False
    