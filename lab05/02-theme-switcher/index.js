/*
    Hints: 
    1. Attach click event handlers to all four of the 
       buttons (#default, #ocean, #desert, and #high-contrast).
    2. Modify the className property of the body tag 
       based on the button that was clicked.
*/

const oceanTheme = (ev) => {
   document.querySelector('body').className = 'ocean';
};

const desertTheme = (ev) => {
   document.querySelector('body').className = 'desert';
};

const highContrastTheme = (ev) => {
   document.querySelector('body').className = 'high-contrast';
};

const defaultTheme = (ev) => {
   document.querySelector('body').className = '';
};

document.querySelector('#default').addEventListener('click', defaultTheme);
document.querySelector('#ocean').addEventListener('click', oceanTheme);
document.querySelector('#desert').addEventListener('click', desertTheme);
document.querySelector('#high-contrast').addEventListener('click', highContrastTheme);