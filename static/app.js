const input1 = document.getElementById("input1"); //file
const input2 = document.getElementById("input2"); //file
const img1 = document.getElementById("img1"); //img no change
const img2 = document.getElementById("img2"); //img no change
const img1transform = document.getElementById("img1transform"); //img change
const img2transform = document.getElementById("img2transform"); //img change
// const form1 = document.getElementById('form1');
const img1component = document.getElementById("img1component");
const img2component = document.getElementById("img2component");

const formData1 = new FormData();
formData1.append("file", "");
formData1.append("component", "");
const formData2 = new FormData();
formData2.append("file", "");
formData2.append("component", "");

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
    index===0? formData1.set("file", file):formData2.set("file", file);
    if(index===0){
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
      reader.addEventListener('load', () => {
        img2.src = reader.result;
      });
        reader.readAsDataURL(file);
    }
  })
})

document.querySelectorAll(".mixerimage").forEach((imageSelector,index)=>{
imageSelector.addEventListener("change",()=>{
  const selectedOutput = document.querySelector(".selectmixeroutput").value;
  const selectedImage=imageSelector.value
  const selectedComponent=document.querySelectorAll(".mixercomponent")[index].value;
  const sliderValue = document.querySelectorAll(".mixerrange")[index].value;
})
});

document.querySelectorAll(".mixercomponent").forEach((componentSelector, index) => {
  componentSelector.addEventListener("change", () => {
    const selectedOutput = document.querySelector(".selectmixeroutput").value;
    const selectedImage =document.querySelectorAll(".mixerimage")[index].value.value;
    const selectedComponent = componentSelector.value;
    const sliderValue = document.querySelectorAll(".mixerrange")[index].value;
  });
});

document.querySelectorAll(".mixerrange").forEach((ratioslider, index) => {
  ratioslider.addEventListener("change", () => {
    const selectedOutput = document.querySelector(".selectmixeroutput").value;
    const selectedImage = document.querySelectorAll(".mixerimage")[index].value.value;
    const selectedComponent = document.querySelectorAll(".mixercomponent")[index].value;
    const sliderValue = ratioslider.value;
  });
});

// document.querySelector(".selectmixeroutput").addEventListener("change",()=>{
//   const selectedOutput = document.querySelector(".selectmixeroutput").value;

// })
// //output mixer
// const outputSelect = document.getElementById("output-select");
// const component1Select = document.getElementById("component1-select");
// const component1Range = document.getElementById("component1-range");
// const component1Type = document.getElementById("component1-type");
// const component2Select = document.getElementById("component2-select");
// const component2Range = document.getElementById("component2-range");
// const component2Type = document.getElementById("component2-type");
// const output1 = document.getElementById("output1");
// const output2 = document.getElementById("output2");

// outputSelect.addEventListener("change", () => {
//   const outputNum = outputSelect.value;
//   const component1 = component1Select.value;
//   const component1Value = component1Range.value;
//   const component1TypeValue = component1Type.value;
//   const component2 = component2Select.value;
//   const component2Value = component2Range.value;
//   const component2TypeValue = component2Type.value;

//   fetch("/mix_images", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({
//       output_num: outputNum,
//       component1: component1,
//       component1_value: component1Value,
//       component1_type: component1TypeValue,
//       component2: component2,
//       component2_value: component2Value,
//       component2_type: component2TypeValue,
//     }),
//   })
//     .then((response) => response.json())
//     .then((data) => {
//       if (outputNum === "1") {
//         output1.src = "data:image/png;base64," + data.output_image;
//       } else if (outputNum === "2") {
//         output2.src = "data:image/png;base64," + data.output_image;
//       }
//     });
// });
