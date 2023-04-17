// // function myFunction() {
// //     document.getElementById("myDropdown").classList.toggle("show");
// //   }
  
// //   window.onclick = function(event) {
// //     if (!event.target.matches('.dropbtn')) {
// //       var dropdowns = document.getElementsByClassName("dropdown-content");
// //       for (var i = 0; i < dropdowns.length; i++) {
// //         var openDropdown = dropdowns[i];
// //         if (openDropdown.classList.contains('show')) {
// //           openDropdown.classList.remove('show');
// //         }
// //       }
// //     }
// //   }


//   const inputBox = document.getElementById('text');
//       const outputDiv = document.getElementById('output');
//       let predictionElement = null;
  
//       inputBox.addEventListener('input', () => {
//         const inputText = inputBox.value;
//         if (inputText.trim() === '') {
//           hidePrediction();
//           return;
//         }
  
//         fetch('/predict', {
//           method: 'POST',
//           headers: {'Content-Type': 'application/x-www-form-urlencoded'},
//           body: `text=${encodeURIComponent(inputText)}`
//         })
//         .then(response => response.json())
//         .then(data => {
//           const prediction = data.output;
//           if (prediction !== '') {
//             showPrediction(prediction);
//           } else {
//             hidePrediction();
//           }
//         })
//         .catch(error => console.error(error));
//       });
  
//       inputBox.addEventListener('keydown', event => {
//         if (event.key === 'Escape') {
//           hidePrediction();
//         } else if (predictionElement !== null && (event.key === 'Tab' || event.key === 'Enter')) {
//           event.preventDefault();
//           replaceWord(predictionElement.textContent);
//           hidePrediction();
//         }
//       });
  
//       function showPrediction(prediction) {
//         if (predictionElement === null) {
//           predictionElement = document.createElement('span');
//           predictionElement.classList.add('prediction');
//           document.body.appendChild(predictionElement);
//         }
//         predictionElement.textContent = prediction;
//         const inputRect = inputBox.getBoundingClientRect();
//         const cursorPosition = inputBox.selectionStart;
//         const cursorRect = getRectAtPosition(inputBox, cursorPosition);
//         const left = inputRect.left + cursorRect.left + window.pageXOffset;
//         const top = inputRect.top + cursorRect.bottom + window.pageYOffset;
//         const inputText = inputBox.value.trim().replace(/\s+/g, ' ');

//         predictionElement.style.left = `${left}px`;
//         predictionElement.style.top = `${top}px`;
//         predictionElement.addEventListener('mousedown', preventDefault);
//         predictionElement.addEventListener('mouseup', preventDefault);
//         predictionElement.addEventListener('click', () => {
//           replaceWord(predictionElement.textContent);
//           hidePrediction();
//         });
//       }

   

//       function getRectAtPosition(element, position) {
//         const range = document.createRange();
//         range.setStart(element, position);
//         range.setEnd(element, position);
//         return range.getBoundingClientRect();
//       }
  
//       function hidePrediction() {
//         if (predictionElement !== null) {
//           predictionElement.parentNode.removeChild(predictionElement);
//           predictionElement = null;
//         }
//       }
  
//       function replaceWord(word) {
//         const textBeforeCursor = inputBox.value.slice(0, inputBox.selectionStart);
//         const textAfterCursor = inputBox.value.slice(inputBox.selectionEnd);
//         const lastSpaceIndex = textBeforeCursor.lastIndexOf(' ');
//         const prefix = textBeforeCursor.slice(0, lastSpaceIndex + 1);
//         const suffix = textBeforeCursor.slice(inputBox.selectionStart);
//         const newText = `${prefix}${word}${suffix}${textAfterCursor}`;
//         inputBox.value = newText;
//         inputBox.selectionStart = prefix.length + word.length;
//         inputBox.selectionEnd = inputBox.selectionStart;
//         inputBox.focus();
//       }
  
//       function preventDefault(event) {
//         event.preventDefault();
//       }