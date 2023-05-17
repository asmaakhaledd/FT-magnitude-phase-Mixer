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
        self.modeArr = [["Real", "Imaginary"],["Imaginary", "Real"],["Magnitude", "Phase"],["Phase", "Magnitude"],["Uniform Magnitude", "Uniform Phase"],["Uniform Magnitude", "Phase"],["Phase","Uniform Magnitude" ],["Uniform Phase", "Uniform Magnitude"]];

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
    def mix_components(self, component1, component2, component1obj, component2obj, str_ratioI, str_ratioII):
        ratioI = int(str_ratioI)
        ratioII = int(str_ratioII)
        total = ratioI + ratioII
        ratio1 = ratioI / total
        ratio2 = ratioII / total
        
        comp1pt1 = component1obj.component_result(component1)
        comp1pt2 = component1obj.component_result(component2)
        comp2pt1 = component2obj.component_result(component1)
        comp2pt2 = component2obj.component_result(component2)

        if component1 == "Magnitude":
            comp1pt1 = np.abs(component1obj.return_fft_shift())
        elif component2 == "Magnitude":
            comp2pt1 = np.abs(component2obj.return_fft_shift())

        mixedpt1 = (1 - ratio1) * comp1pt1 + ratio2 * comp2pt1
        mixedpt2 = ratio1 * comp1pt2 + (1 - ratio2) * comp2pt2

        try:
            index = self.modeArr.index([component1, component2])
            combined = np.multiply(mixedpt1, np.exp(1j * mixedpt2))
            if index == 0 or index == 1:
                combined = mixedpt1 + mixedpt2 * 1j
                print(index)
            ft_shift = np.fft.fftshift(combined)
            mixInverse = np.real(np.fft.ifft2(ft_shift))
            normalized = cv2.normalize(mixInverse, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            retval, buffer = cv2.imencode('.jpg', normalized)
            response = buffer.tobytes()
            logging.info("Applied transformation on image")
            return response
        except ValueError:
            logging.error("Invalid Fourier components")
            return None


        
            # if((component1=="Magnitude" and component2=="Phase") or (component2=="Magnitude" and component1=="Phase")):
            #     mag1=np.abs(component1obj.return_fft_shift())
            #     ph1=component1obj.component_result("Phase")
            #     mag2=np.abs(component2obj.return_fft_shift())
            #     ph2=component2obj.component_result("Phase")
            #     mag_mix = (1-ratio1) * mag1 +  (ratio2) * mag2
            #     ph_mix=(ratio1) * ph1 +  (1-ratio2) *ph2
            #     combined = np.multiply(mag_mix, np.exp(1j * ph_mix))
            # elif((component1=="Uniform Magnitude" and component2=="Uniform Phase") or (component2=="Uniform Magnitude" and component1=="Uniform Phase")):
            #     uni_mag1=component1obj.component_result("Uniform Magnitude")
            #     uni_ph1=component1obj.component_result("Uniform Phase")
            #     uni_mag2=component2obj.component_result("Uniform Magnitude")
            #     uni_ph2=component2obj.component_result("Uniform Phase")
            #     mag_mix = (1 - ratio1) * uni_mag1 +  (ratio2) * uni_mag2
            #     ph_mix=(ratio1) * uni_ph1 +  (1 -ratio2) *uni_ph2
            #     combined = np.multiply(mag_mix, np.exp(1j * ph_mix))
            # elif((component1=="Uniform Magnitude" and component2=="Phase") or (component2=="Uniform Magnitude" and component1=="Phase")):
            #     uni_mag1=component1obj.component_result("Uniform Magnitude")
            #     uni_ph1=component1obj.component_result("Phase")
            #     uni_mag2=component2obj.component_result("Uniform Magnitude")
            #     uni_ph2=component2obj.component_result("Phase")
            #     mag_mix = (1 - ratio1) * uni_mag1 +  (ratio2) * uni_mag2
            #     ph_mix=(ratio1) * uni_ph1 +  (1 -ratio2) *uni_ph2
            #     combined = np.multiply(mag_mix, np.exp(1j * ph_mix))    
            # elif((component1=="Magnitude" and component2=="Uniform Phase") or (component2=="Magnitude" and component1=="Uniform Phase")):
            #     uni_mag1=np.abs(component1obj.return_fft_shift())
            #     uni_ph1=component1obj.component_result("Uniform Phase")
            #     uni_mag2=np.abs(component2obj.return_fft_shift())
            #     uni_ph2=component2obj.component_result("Uniform Phase")
            #     mag_mix = (1 - ratio1) * uni_mag1 +  (ratio2) * uni_mag2
            #     ph_mix=(ratio1) * uni_ph1 +  (1 -ratio2) *uni_ph2
            #     combined = np.multiply(mag_mix, np.exp(1j * ph_mix))                
            # elif(component1=="Real" and component2=="Imaginary" or component2=="Real" and component1=="Imaginary"):
            #     real1=component1obj.component_result("Real")
            #     img1=component1obj.component_result("Imaginary")
            #     real2=component2obj.component_result("Real")
            #     img2=component2obj.component_result("Imaginary")
            #     real_mix = (1-ratio1) * real1 +  (ratio2) * real2
            #     img_mix=(ratio2) * img1 +  (1-ratio2) *img2
            #     combined = real_mix + img_mix * 1j

            # if combined is None:
            #     logging.error("Invalid Fourier components COMBINED")
            #     return None
            # ft_shift = np.fft.fftshift(combined) 
            # mixInverse = np.real(np.fft.ifft2(ft_shift))
            # # return mixed_img
            # # norm = cv2.normalize(mixInverse, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            # retval, buffer = cv2.imencode('.jpg', mixInverse)
            # response = buffer.tobytes()
            # logging.info(f"Applied transformation on image")
            # return response
