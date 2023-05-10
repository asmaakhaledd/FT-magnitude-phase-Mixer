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

    # def mix_components(self, resultI, resultII, fft1, fft2, str_ratioI, str_ratioII):
    #     # Check if the input parameters are valid
    #     if resultI is None or resultII is None or fft1 is None or fft2 is None:
    #         logging.error("Invalid input parameters")
    #         return None
    #     ratioI = int(str_ratioI)
    #     ratioII = int(str_ratioII)# zero condition test case
    #     total = ratioI + ratioII
    #     ratio1 = ratioI / total
    #     ratio2 = ratioII / total
    #     # Mix the two component results
    #     mixed_result = cv2.addWeighted(resultI, ratio1, resultII, ratio2, 0)
    #     # Create a three-channel array representing the mixed Fourier transform
    #     mixed_fft = np.zeros((fft1.shape[0], fft1.shape[1], 3), dtype=np.float32)
    #     mixed_fft[:, :, 1] = fft2.real
    #     mixed_fft[:, :, 2] = fft2.imag
    #     mixed_fft[:, :, 0] = mixed_result

    #     # Inverse Fourier transform to get the mixed image
    #     mixed_image = np.fft.ifft2(np.fft.ifftshift(mixed_fft[:, :, 0] + mixed_fft[:, :, 1]*1j + mixed_fft[:, :, 2]*1j)).real
    #     # Normalize the image and return it
    #     norm = cv2.normalize(mixed_image, None, 0, 1, cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    #     norm = (255*norm).astype(np.uint8)
    #     retval, buffer = cv2.imencode('.jpg', norm)
    #     response = buffer.tobytes()
    #     logging.info(f"Applied transformation on image")
    #     return response





    # def mix_components(self, resultI, resultII, fft1, fft2, str_ratioI, str_ratioII):
    #     # Calculate the mixing ratio
    #     ratioI=int(str_ratioI)
    #     ratioII=int(str_ratioII)
    #     print("ratio1",ratioI)
    #     print("ratio2",ratioII)
    #     total = ratioI + ratioII
    #     ratio1 = ratioI / total
    #     ratio2 = ratioII / total
    #    # Mix the two Fourier transforms according to the given ratios
    #     mixed_ft = ratio1 * resultI + ratio2 * resultII
    #    # Inverse Fourier transform to get the mixed image
    #     mixed_image = np.fft.ifft2(mixed_ft).real
    #    # Normalize the image and return it
    #     norm = cv2.normalize(mixed_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    #     retval, buffer = cv2.imencode('.jpg', norm)
    #     response = buffer.tobytes()
    #     logging.info(f"Applied transformation on image")
    #     return response
    
    #     # return mixed_image

    # def mixer(self,image1bytes,image2bytes,str_ratio1,str_ratio2):
    #     # Decode the image bytes into numpy arrays
    #     ratio1=int(str_ratio1)
    #     ratio2=int(str_ratio2)
    #     component_one_image = cv2.imdecode(np.frombuffer(image1bytes, np.uint8), cv2.IMREAD_GRAYSCALE)
    #     component_two_image = cv2.imdecode(np.frombuffer(image2bytes, np.uint8), cv2.IMREAD_GRAYSCALE)
    #     image1 = np.float32(component_one_image)
    #     image2 = np.float32(component_two_image)
    #     # Calculate the weighted sum of the two images
    #     mixed_image = cv2.addWeighted(image1, ratio1 / 100, image2, ratio2 / 100, 0)

    #     # Normalize the mixed image
    #     mixed_image_norm = cv2.normalize(mixed_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    #     # Encode the mixed image as a JPEG and return it as a response
    #     retval, buffer = cv2.imencode('.jpg', mixed_image_norm)
    #     response = buffer.tobytes()
    #     return response

  
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
                mag_mix = (1 - ratio1) * mag1 +  (ratio2) * mag2
                ph_mix=(ratio1) * ph1 +  (1 -ratio2) *ph2
                combined = np.multiply(mag_mix, np.exp(1j * ph_mix))
            elif(component1=="Real" and component2=="Imaginary" or component2=="Real" and component1=="Imaginary"):
                real1=component1obj.component_result("Magnitude")
                img1=component1obj.component_result("Phase")
                real2=component2obj.component_result("Magnitude")
                img2=component2obj.component_result("Phase")
                real_mix = (ratio1) * real1 +  (1 - ratio2) * real2
                img_mix=(ratio1) * img1 +  (1 -ratio2) *img2
                combined = real_mix + img_mix * 1j
            if combined is None:
                logging.error("Invalid Fourier components")
                return None
            mixInverse = np.real(np.fft.ifft2(combined))
            # return mixed_img
            norm = cv2.normalize(mixInverse, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            retval, buffer = cv2.imencode('.jpg', norm)
            response = buffer.tobytes()
            logging.info(f"Applied transformation on image")
            return response
    
    # def mix(self, image2:'Image', mag_real_ratio, ph_img_ratio, mode):
    #     w1 = mag_real_ratio
    #     w2 = ph_img_ratio        
    #     mixInverse = None

    #     if mode == "magnitudeandphase" or mode == "phaseandmagnitude":
            
    #         M1 = self.magnitude
    #         M2 = image2.magnitude

    #         P1 = self.phase
    #         P2 = image2.phase

    #         magnitudeMix = w1*M1 + (1-w1)*M2
    #         phaseMix = (1-w2)*P1 + w2*P2

    #         combined = np.multiply(magnitudeMix, np.exp(1j * phaseMix))
            
    #     elif mode == "realandimaginary" or mode == "imaginaryandreal":

    #         R1 = self.real
    #         R2 = image2.real

    #         I1 = self.imaginary
    #         I2 = image2.imaginary

    #         realMix = w1*R1 + (1-w1)*R2
    #         imaginaryMix = (1-w2)*I1 + w2*I2

    #         combined = realMix + imaginaryMix * 1j
            
    #     #must set sliders to zeros 
    #     elif mode == "magnitudeanduniform phase":
            
    #         M1 = self.magnitude
    #         M2 = image2.magnitude
            
    #         magnitudeMix = w2*M1 + (1-w2)*M2
            
    #         combined = np.multiply(magnitudeMix, np.exp(1j * image2.uniform_phase))
            
    #     elif mode == "uniform phaseandmagnitude" :
            
    #         M1 = self.magnitude
    #         M2 = image2.magnitude
            
    #         magnitudeMix = w1*M1 + (1-w1)*M2
            
    #         combined = np.multiply(magnitudeMix, np.exp(1j * self.uniform_phase))

    #     elif mode == "uniform magnitudeandphase" :
            
    #         P1 = self.phase
    #         P2 = image2.phase
            
    #         phaseMix = (1-w2)*P1 + w2*P2
            
    #         combined = np.multiply(self.uniform_magnitude, np.exp(1j * phaseMix))

    #     elif mode == "phaseanduniform magnitude":
            
    #         P1 = self.phase
    #         P2 = image2.phase
            
    #         phaseMix = (1-w1)*P1 + w1*P2
            
    #         combined = np.multiply(image2.uniform_magnitude, np.exp(1j * phaseMix))
        
    #     mixInverse = np.real(np.fft.ifft2(combined))
    #     return abs(mixInverse)