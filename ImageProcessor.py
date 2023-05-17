import numpy as np
import cv2
import logging

# Setup logging configuration
logging.basicConfig(filename='image_processor.log', level=logging.INFO)

# Create ImageProcessor class
class ImageProcessor:
     # Constructor for ImageProcessor class
    def __init__(self):
        self.image = None 
        self.ft = None
        self.ft_shift=None

  # Function to perform Fourier transform
    def perform_fft(self):
        self.ft = np.fft.fft2(self.image)
        self.ft_shift = np.fft.fftshift(self.ft)    

  # Function to open image
    def open_image(self, file) -> bool:
        print(file)
        self.image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
        if self.image is None:
            logging.error(f"Failed to open image")
            return False
        logging.info(f"Opened image")
        return True

 # Function to display image
    def display_image(self, component):
        result=self.component_result(component)
        norm = cv2.normalize(result, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        retval, buffer = cv2.imencode('.jpg', norm)
        response = buffer.tobytes()
        logging.info(f"Applied transformation on image")
        return response

# Function to get component result
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
        # elif component == "Uniform Magnitude":
        #     magnitude = np.abs(self.ft_shift)
        #     result = np.ones_like(magnitude)
        # elif component == "Uniform Phase":
        #     phase =  np.angle(self.ft_shift)
        #     result= np.zeros_like(phase)
        elif component == "Uniform Magnitude":
            magnitude = np.abs(self.ft_shift)
            uniform_magnitude = np.ones_like(magnitude) 
            result = magnitude / uniform_magnitude
        elif component == "Uniform Phase":
            #Uniform phase refers to a transformation applied to the phase spectrum of an image such that all the phase values become uniformly distributed across the spectrum. This is done to remove any abrupt changes in the phase of the image, which can cause artifacts or distortions in the reconstructed image.
            phase =  np.angle(self.ft_shift)
            # #calculate the uniform phase spectrum by taking the exponential of the angle of the Fourier transform coefficients to create a phase spectrum with a more uniform distribution of values
            # uniform_phase = np.exp(1j * phase)
            # # create a new Fourier transform with a more uniform phase spectrum
            # new_ft_shift=self.ft * uniform_phase
            # #get the angle/phase of the uniform phase new ft
            # result = np.angle(new_ft_shift)
            result = np.multiply(phase , 0)
        else:
            logging.warning(f"Invalid component: {component}") # warn the user of an invalid component
            return None
        return result

    # Function to return the Fourier Transform result
    def return_fft(self):
        return self.ft
    
    def return_fft_shift(self):
        return self.ft_shift

    # Function to mix two Fourier Transform components based on given ratios
    def mix_components(self,component1,component2,component1obj,component2obj,str_ratioI, str_ratioII):
            ratioI = int(str_ratioI)
            ratioII = int(str_ratioII)# zero condition test case
            total = ratioI + ratioII
            ratio1 = ratioI / total 
            ratio2 = ratioII / total
            combined = None  # Initialize combined with a default value
            # Mix two Fourier Transform components based on given ratios and component types
           
           
        
            def mix_components_helper(component1_type, component2_type, op1, op2,op3,op4):
             
             if (component1 == component1_type and component2 == component2_type) or (component2 == component1_type and component1 == component2_type):
                # op1_1 = component1obj.component_result(component1_type)
                # op1_2 = component2obj.component_result(component1_type)
                # op2_1 = component1obj.component_result(component2_type)
                # op2_2 = component2obj.component_result(component2_type)
                op1_mix = (1 - ratio1) * op1 + ratio2 * op3
                op2_mix = ratio1 * op2 + (1 - ratio2) * op4
                if (component1_type=="Real") or (component1_type=="Imaginary"):
                    return  op1_mix + op2_mix * 1j
                else:
                    return  np.multiply(op1_mix, np.exp(1j * op2_mix))
            components = [
            ("Magnitude", "Phase", np.abs(component1obj.return_fft_shift()), component1obj.component_result("Phase"),np.abs(component2obj.return_fft_shift()), component2obj.component_result("Phase")),
            ("Uniform Magnitude", "Uniform Phase", component1obj.component_result("Uniform Magnitude"), component1obj.component_result("Uniform Phase"), component2obj.component_result("Uniform Magnitude"), component2obj.component_result("Uniform Phase")),
            ("Uniform Magnitude", "Phase", component1obj.component_result("Uniform Magnitude"), component1obj.component_result("Phase"), component2obj.component_result("Uniform Magnitude"), component2obj.component_result("Phase")),
            ("Magnitude", "Uniform Phase", np.abs(component1obj.return_fft_shift()), component1obj.component_result("Uniform Phase"), np.abs(component2obj.return_fft_shift()), component2obj.component_result("Uniform Phase")),
            ("Real", "Imaginary", component1obj.component_result("Real"), component1obj.component_result("Imaginary"), component2obj.component_result("Real"), component2obj.component_result("Imaginary"))]
            
            # combined = None
            for component in components:
                component1_type, component2_type, op1, op2, op3, op4 = component
                combined = mix_components_helper(component1_type, component2_type, op1, op2, op3, op4)
                if combined is not None:
                    break
               
            if combined is None:
                logging.error("Invalid Fourier components")
                return None

    
            ft_shift = np.fft.fftshift(combined)
            mixInverse = np.real(np.fft.ifft2(ft_shift))
            norm = cv2.normalize(mixInverse, None, 0, 255, cv2.NORM_MINMAX)
            retval, buffer = cv2.imencode('.jpg', mixInverse)
            response = buffer.tobytes()
            logging.info("Applied transformation on image")
            return response
