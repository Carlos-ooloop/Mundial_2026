const form = document.querySelector('form');
const nameInput = document.getElementById('name');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const messageInput = document.getElementById('message');

function validateName() {
    const value = nameInput.value.trim();
    if (value === '') {
        nameInput.setCustomValidity('El nombre es obligatorio');
        nameInput.reportValidity();
        return false;
    }
    nameInput.setCustomValidity('');
    return true;
}

function validateEmail() {
    const value = emailInput.value.trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (value === '' || !emailRegex.test(value)) {
        emailInput.setCustomValidity('Introduce un email válido');
        emailInput.reportValidity();
        return false;
    }
    emailInput.setCustomValidity('');
    return true;
}

function validatePassword() {
    const value = passwordInput.value;
    if (value === '') {
        passwordInput.setCustomValidity('La contraseña es obligatoria');
        passwordInput.reportValidity();
        return false;
    }
    passwordInput.setCustomValidity('');
    return true;
}

function validateMessage() {

    return true;
}

function validateForm() {
    return validateName() && validateEmail() && validatePassword() && validateMessage();
}

form.addEventListener('submit', function (event) {
    event.preventDefault();

    if (!validateForm()) {
        return;
    }

    const formData = {
        name: nameInput.value.trim(),
        email: emailInput.value.trim(),
        password: passwordInput.value,
        message: messageInput.value.trim(),
    };

    console.log('Datos del formulario:', formData);

    // Ocultar formulario y mostrar página principal
    form.style.display = 'none';
    document.getElementById('homepage').style.display = 'block';
    
});

