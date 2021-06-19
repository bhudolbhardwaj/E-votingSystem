const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');
const name = document.getElementById('name');
const mobile = document.getElementById('mobile');
const state = document.getElementById('state');
const date = document.getElementById('date');
// const form = document.getElementById('form');
const status = false;


signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

const loginscan = document.getElementById('scanform');
function handleForm(event) { event.preventDefault(); } 
loginscan.addEventListener('submit', handleForm);

