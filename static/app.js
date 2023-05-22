const input1 = document.getElementById("input1"); //file
const input2 = document.getElementById("input2"); //file
const img1 = document.getElementById("img1"); //img no change
const img2 = document.getElementById("img2"); //img no change
const img1transform = document.getElementById("img1transform"); //img change
const img2transform = document.getElementById("img2transform"); //img change
// const form1 = document.getElementById('form1');
const img1component = document.getElementById("img1component");
const img2component = document.getElementById("img2component");

const outputSelector = document.getElementById("selectoutputmixer");
const imageSelectorOne=document.getElementById("imageselector1");
const imageSelectorTwo = document.getElementById("imageselector2");
const componentSelectorOne = document.getElementById("componentselector1");
const componentSelectorTwo=document.getElementById("componentselector2");
const ratioSliderOne=document.getElementById("ratioslider1");
const ratioSliderTwo = document.getElementById("ratioslider2");

const output1 = document.getElementById("output1");
const output2 = document.getElementById("output2");

const formData1 = new FormData();
formData1.append("file", "");
formData1.append("component", "");
const formData2 = new FormData();
formData2.append("file", "");
formData2.append("component", "");
let imageFile1;
let imageFile2;

let formDataMix = new FormData();
formDataMix.append("image1", "");
formDataMix.append("component1", "Magnitude");
formDataMix.append("ratio1", 0);
formDataMix.append("image2", "");
formDataMix.append("component2", "Magnitude");
formDataMix.append("ratio2", 0);

const modeArr = [
  ["Magnitude", "Phase"],
  ["Phase", "Magnitude"],
  ["Real", "Imaginary"],
  ["Imaginary", "Real"],
  ["Uniform Magnitude", "Uniform Phase"],
  ["Uniform Magnitude", "Phase"],
  ["Uniform Phase","Magnitude" ],
  ["Uniform Phase", "Uniform Magnitude"],
];

// Select all elements with the "imagecomponent" class and add a change event listener to each one 
document.querySelectorAll(".imagecomponent").forEach((component,index)=>{
  component.addEventListener("change",()=>{
     // Get the value of the selected option
    const selectedComponent = component.value;
     // Create a new FormData object to send data to the server
    let formData = new FormData();
    // Declare a variable to hold the image transform element
    let imgTransform;
    // If this is the first element in the list
    if (index === 0) {
      // Set the "component" key in formData1 to the selected option value
      formData1.set("component", selectedComponent);
      // Use formData1 and img1transform for this element
      formData = formData1;
      imgTransform = img1transform;
    } else {
      // Set the "component" key in formData2 to the selected option value
      formData2.set("component", selectedComponent);
      // Use formData2 and img2transform for this element
      formData = formData2;
      imgTransform = img2transform;
    }
    // Send a POST request to the server with the FormData object as the request body
    fetch("/process_image", {
      method: "POST",
      body: formData,
    }).then((response) => response.blob())// Extract the image data from the response as a Blob object
      .then((data) => {
          console.log("img",data)
          const url = URL.createObjectURL(data); // Create a URL for the image data
          // Update the image transform variable with the new URL
          imgTransform.src = url;
        });
  })
});

// Add event listener to all elements with the "fileinput" class
document.querySelectorAll(".fileinput").forEach((input,index)=>{
  input.addEventListener("change",()=>{
    // Get the selected file
    const file = input.files[0];
    const reader = new FileReader();
    // index===0? formData1.set("file", file):formData2.set("file", file);
    // index === 0 ? (imageFile1 = file) : imageFile2=file ;
    // Set the file object to the correct FormData object and imageFile variable based on the index
    if(index===0){
      // Set the file object to the formData1 object
      formData1.set("file", file);
      // Set the imageFile1 variable to the file object
      imageFile1 = file;
      // Set the image1 and image2 keys in the formDataMix object to the imageFile1 variable
      formDataMix.set("image1", imageFile1);
      formDataMix.set("image2", imageFile1);
      // Add a listener for the "load" event on the reader object
      reader.addEventListener('load', () => {
        // Set the src attribute of the img1 element to the result of the reader object
        img1.src = reader.result;
      });
      // Read the file as a data URL
      reader.readAsDataURL(file);
    }
    else{
      // Add a listener for the "load" event on the img2 element
      img2.onload = () => {
      // Check if the dimensions of the img2 element match those of the img1 element
      if (img2.naturalWidth !== img1.naturalWidth || img2.naturalHeight !== img1.naturalHeight) {
        alert("Image size does not match!");
        img2.src="";
        return;
      }
    }
     // Set the file object to the formData2 object
     formData2.set("file", file);
     // Set the imageFile2 variable to the file object
     imageFile2 = file;
     // Add a listener for the "load" event on the reader object
     reader.addEventListener('load', () => {
       // Set the src attribute of the img2 element to the result of the reader object
       img2.src = reader.result;
     });
     // Read the file as a data URL
     reader.readAsDataURL(file);
    }
  })
})

  // Loop over all elements with class "mixerimage"
  document.querySelectorAll(".mixerimage").forEach((image, index) => {
  // Add an event listener to each element when it changes
    image.addEventListener("change",()=>{
    // Check if this is the first or second image input element
    if(index==0){
    // If the selected value is "img1", add the first image file to the form data, otherwise add the second image file
      image.value == "img1"
        ? formDataMix.set("image1", imageFile1)
        : formDataMix.set("image1", imageFile2);
    }else{
      image.value == "img1"
        ? formDataMix.set("image2", imageFile1)
        : formDataMix.set("image2", imageFile2);
    }
    // Call the mixImages function to update the output image
    mixImages();
    })
  });


// Listen for change events on all elements with class "mixercomponent"
  document.querySelectorAll(".mixercomponent").forEach((component, index) => {
    component.addEventListener("change", () => {
      // If the first component is changed, set "component1" in the form data
      if (index == 0) {
        formDataMix.set("component1",component.value); 
      } else {
        // Otherwise, set "component2" in the form data
        formDataMix.set("component2", component.value); 
      }
      let combination=[formDataMix.get("component1"),formDataMix.get("component2")]
      let exists = modeArr.some(
        (arr) => arr[0] === combination[0] && arr[1] === combination[1]
      );
        exists?mixImages():alert("Components cannot be mixed")
      // Call the mixImages function to mix the images with the updated form data
        // mixImages();
    });
  });

  // Listen for change events on all elements with class "mixerrange"
  document.querySelectorAll(".mixerrange").forEach((slider, index) => {
    slider.addEventListener("change", () => {
      // If the first slider is changed, set "ratio1" in the form data
      if (index == 0) {
        formDataMix.set("ratio1", slider.value);
      } else {
        // Otherwise, set "ratio2" in the form data
        formDataMix.set("ratio2", slider.value);
      }
      //selects all the elements with the class "slidervalue" and sets their innerHTML to the value of the current slider's value plus the percent symbol
      document.querySelectorAll(".slidervalue")[index].innerHTML=`${slider.value}%`;
       // Call the mixImages function to mix the images with the updated form data
      mixImages();
    });
  });

  // Listen for change events on the outputSelector element
outputSelector.addEventListener("change", () => {
  // Call the mixImages function to mix the images with the updated form data and update the output image
  mixImages();
})

// Function to mix the images with the current form data
function mixImages() {
  // Send a POST request to "/fftmixer" with the current form data
  fetch("/fftmixer", {
    method: "POST",
    body: formDataMix,
  })
    .then((response) => response.blob())
    .then((result) => {
      // Convert the response blob to a URL and set it as the source of the output image element
        const url = URL.createObjectURL(result);
        document.getElementById(outputSelector.value).src = url;
      });
  }

