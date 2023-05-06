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
        print(file)
        self.image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
        if self.image is None:
            logging.error(f"Failed to open image")
            return False
        logging.info(f"Opened image")
        return True

    def display_image(self, component):
        result=self.component_result(component)
        norm = cv2.normalize(result, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        retval, buffer = cv2.imencode('.jpg', norm)
        response = buffer.tobytes()
        logging.info(f"Applied transformation on image")
        return response

    def component_result(self, component):
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
        return result


    def return_fft(self):
        return self.ft


    def mix_components(self, resultI, resutII, fft1, fft2, str_ratioI, str_ratioII):
        # Calculate the mixing ratio
        ratioI=int(str_ratioI)
        ratioII=int(str_ratioII)
        print("ratio1",ratioI)
        print("ratio2",ratioII)
        total = ratioI + ratioII
        ratio1 = ratioI / total
        ratio2 = ratioII / total
       # Mix the two Fourier transforms according to the given ratios
        mixed_ft = ratio1 * fft1 + ratio2 * fft2
       # Inverse Fourier transform to get the mixed image
        mixed_image = np.fft.ifft2(mixed_ft).real
       # Normalize the image and return it
        mixed_image = cv2.normalize(mixed_image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        return mixed_image

  

  
