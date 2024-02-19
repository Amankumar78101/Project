
const wrapper = document.querySelector('.wrapper');
const registerLink = document.querySelector('.register-link');  // Updated class
const loginLink = document.querySelector('.login-link');  // Updated class
// const forgotPassRememberMe = document.querySelector('.forgot-pass-remember-me')


registerLink.onclick=() => {
    wrapper.classList.add('active');    
    // forgotPassRememberMe.classList.add('active');    
}



loginLink.onclick=() => {
    wrapper.classList.remove('active');
    // forgotPassRememberMe.classList.remove('active');
}

registerLink.addEventListener('click',() => {
    // forgotPassRememberMe.style.display = 'none';
})

loginLink.addEventListener('click',() => {
    // forgotPassRememberMe.style.display = 'block';
})