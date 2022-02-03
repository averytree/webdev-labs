let currentFont = 1.4;

const makeBigger = (ev) => {
   currentFont += 0.2;
   setFont();
};

const makeSmaller = (ev) => {
   currentFont -= 0.2;
   setFont();
};

const setFont = () => {
   document.querySelector(".content").style.fontSize =  `${currentFont}em`;
   document.querySelector("h1").style.fontSize = `${currentFont + 0.5}em`;
}


document.querySelector("#a1").addEventListener('click', makeBigger);
document.querySelector("#a2").addEventListener('click', makeSmaller);

