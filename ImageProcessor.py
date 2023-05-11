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
            result = np.abs(self.ft_shift)
        elif component == "Phase":
            #angle of the complex number at each point in the Fourier transformed image. It represents the position of the corresponding frequency component in the image.
            result =  np.angle(self.ft_shift)
        elif component == "Real":
            result =  np.real(self.ft_shift)
        elif component == "Imaginary":
            result =  np.imag(self.ft_shift)
        elif component == "Uniform Magnitude":
            magnitude = np.abs(self.ft_shift)
            result = np.ones_like(magnitude)
        elif component == "Uniform Phase":
            phase =  np.angle(self.ft_shift)
            result= np.zeros_like(phase)
        else:
            logging.warning(f"Invalid component: {component}")
            return None
        return result


    def return_fft(self):
        return self.ft
    
    def mix_components(self,component1,component2,component1obj,component2obj,str_ratioI, str_ratioII):
            # Check if the input parameters are valid
            # if resultI is None or resultII is None:
            #     logging.error("Invalid input parameters")
            #     return None
            ratioI = int(str_ratioI)
            ratioII = int(str_ratioII)# zero condition test case
            total = ratioI + ratioII
            ratio1 = ratioI / total 
            ratio2 = ratioII / total
            combined = None  # Initialize combined with a default value
            if((component1=="Magnitude" and component2=="Phase") or (component2=="Magnitude" and component1=="Phase")):
                mag1=component1obj.component_result("Magnitude")
                ph1=component1obj.component_result("Phase")
                mag2=component2obj.component_result("Magnitude")
                ph2=component2obj.component_result("Phase")
                mag_mix = (ratio1) * mag1 +  (1-ratio1) * mag2
                ph_mix=(1-ratio2) * ph1 +  (ratio2) *ph2
                combined = np.multiply(mag_mix, np.exp(1j * ph_mix))
            elif((component1=="Uniform Magnitude" and component2=="Uniform Phase") or (component2=="Uniform Magnitude" and component1=="Uniform Phase")):
                uni_mag1=component1obj.component_result("Uniform Magnitude")
                uni_ph1=component1obj.component_result("Uniform Phase")
                uni_mag2=component2obj.component_result("Uniform Magnitude")
                uni_ph2=component2obj.component_result("Uniform Phase")
                mag_mix = (1 - ratio1) * uni_mag1 +  (ratio2) * uni_mag2
                ph_mix=(ratio1) * uni_ph1 +  (1 -ratio2) *uni_ph2
                combined = np.multiply(mag_mix, np.exp(1j * ph_mix))    
            elif(component1=="Real" and component2=="Imaginary" or component2=="Real" and component1=="Imaginary"):
                real1=component1obj.component_result("Real")
                img1=component1obj.component_result("Imaginary")
                real2=component2obj.component_result("Real")
                img2=component2obj.component_result("Imaginary")
                real_mix = (ratio1) * real1 +  (1-ratio1) * real2
                img_mix=(1-ratio2) * img1 +  (ratio2) *img2
                combined = real_mix + img_mix * 1j
            if combined is None:
                logging.error("Invalid Fourier components")
                return None
            ft_shift = np.fft.fftshift(combined) 
            mixInverse = np.real(np.fft.ifft2(ft_shift))
            # return mixed_img
            # norm = cv2.normalize(mixInverse, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            retval, buffer = cv2.imencode('.jpg', mixInverse)
            response = buffer.tobytes()
            logging.info(f"Applied transformation on image")
            return response
