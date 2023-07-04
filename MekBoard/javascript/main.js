// window.addEventListener('DOMContentLoaded', () => {
//     console.log('DOMContentLoaded event triggered');
//     // Rest of the code
  
//     // Loop through each div element
//     Array.from(divs).forEach((div) => {
//       // Check the initial height
//       adjustHeight(div);
//     });
    
//     // Check the height whenever the window is resized
//     window.addEventListener('resize', () => {
//       Array.from(divs).forEach((div) => {
//         adjustHeight(div);
//       });
//     });
//   });
  
//   function adjustHeight(element) {
//     const maxHeight = 60; // Maximum height in pixels
    
//     // Reset the height to auto before calculating
//     element.style.height = 'fit-content';
    
//     // Get the computed height of the element
//     const height = element.clientHeight;
    
//     // Set the height based on the condition
//     element.style.height = height > maxHeight ? `${maxHeight}px` : 'fit-content';
//   }
  