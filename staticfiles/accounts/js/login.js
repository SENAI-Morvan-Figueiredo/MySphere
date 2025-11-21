function togglePassword() {
    const passwordInput = document.getElementById('id_password');
    const eyeIcon = document.getElementById('eye-icon');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeIcon.innerHTML = `
            <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
            <line x1="1" y1="1" x2="23" y2="23"></line>
        `;
    } else {
        passwordInput.type = 'password';
        eyeIcon.innerHTML = `
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
            <circle cx="12" cy="12" r="3"></circle>
        `;
    }
}

const rememberCheckbox = document.getElementById('remember');
if (rememberCheckbox) {
    const isRemembered = localStorage.getItem('remember_me');
    if (isRemembered === 'true') {
        rememberCheckbox.checked = true;
    }
    
    rememberCheckbox.addEventListener('change', function() {
        if (this.checked) {
            localStorage.setItem('remember_me', 'true');
        } else {
            localStorage.removeItem('remember_me');
        }
    });
}
