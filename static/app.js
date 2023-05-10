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

document.querySelectorAll(".imagecomponent").forEach((component,index)=>{
  component.addEventListener("change",()=>{
    const selectedComponent = component.value;
    let formData = new FormData();
    let imgTransform;
    if (index === 0) {
      formData1.set("component", selectedComponent);
      formData = formData1;
      imgTransform = img1transform;
    } else {
      formData2.set("component", selectedComponent);
      formData = formData2;
      imgTransform = img2transform;
    }
    fetch("/process_image", {
      method: "POST",
      body: formData,
    }).then((response) => response.blob())
      .then((data) => {
          console.log("img",data)
          const url = URL.createObjectURL(data);
          imgTransform.src = url;
        });
  })
});

document.querySelectorAll(".fileinput").forEach((input,index)=>{
  input.addEventListener("change",()=>{
    const file = input.files[0];
    const reader = new FileReader();
    // index===0? formData1.set("file", file):formData2.set("file", file);
    // index === 0 ? (imageFile1 = file) : imageFile2=file ;
    if(index===0){
      formData1.set("file", file);
      imageFile1 = file;
      formDataMix.set("image1", imageFile1);
      formDataMix.set("image2", imageFile1);
      reader.addEventListener('load', () => {
        img1.src = reader.result;
      });
        reader.readAsDataURL(file);
    }
    else{
      img2.onload = () => {
      if (img2.naturalWidth !== img1.naturalWidth || img2.naturalHeight !== img1.naturalHeight) {
        alert("Image size does not match!");
        img2.src="";
        return;
      }
    }
    formData2.set("file", file);
    imageFile2 = file;
      reader.addEventListener('load', () => {
        img2.src = reader.result;
      });
        reader.readAsDataURL(file);
    }
  })
})

  document.querySelectorAll(".mixerimage").forEach((image, index) => {
    image.addEventListener("change",()=>{
    if(index==0){
      image.value == "img1"
        ? formDataMix.set("image1", imageFile1)
        : formDataMix.set("image1", imageFile2);
    }else{
      image.value == "img1"
        ? formDataMix.set("image2", imageFile1)
        : formDataMix.set("image2", imageFile2);
    }
    mixImages();
    })
  });

  document.querySelectorAll(".mixercomponent").forEach((component, index) => {
    component.addEventListener("change", () => {
      if (index == 0) {
        formDataMix.set("component1",component.value); 
      } else {
        formDataMix.set("component2", component.value); 
      }
      mixImages();
    });
  });

  document.querySelectorAll(".mixerrange").forEach((slider, index) => {
    slider.addEventListener("change", () => {
      if (index == 0) {
        formDataMix.set("ratio1", slider.value);
      } else {
        formDataMix.set("ratio2", slider.value);
      }
      document.querySelectorAll(".slidervalue")[index].innerHTML=`${slider.value}%`;
      mixImages();
    });
  });

  outputSelector.addEventListener("change",()=>{
    mixImages();
  })

  function mixImages(){
    fetch("/fftmixer", {
      method: "POST",
      body: formDataMix,
    })
      .then((response) => response.blob())
      .then((result) => {
        console.log("img", result);
        const url = URL.createObjectURL(result);
        document.getElementById(outputSelector.value).src = url;
      });
  }
