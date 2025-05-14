document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');

    form.addEventListener('submit', function(event) {
        let valid = true;
        const requiredFields = form.querySelectorAll('[required]');

        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                valid = false;
                field.classList.add('error');
            } else {
                field.classList.remove('error');
            }
        });

        if (!valid) {
            event.preventDefault();
            alert('Please fill out all required fields.');
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const phoneInput = document.getElementById('phone');
    
    // Create error message elements
    const nameError = document.createElement('div');
    nameError.className = 'error-message';
    nameError.style.display = 'none';
    nameError.style.color = 'red';
    nameError.style.fontSize = '0.8rem';
    nameError.style.marginTop = '5px';
    
    const emailError = document.createElement('div');
    emailError.className = 'error-message';
    emailError.style.display = 'none';
    emailError.style.color = 'red';
    emailError.style.fontSize = '0.8rem';
    emailError.style.marginTop = '5px';
    
    const phoneError = document.createElement('div');
    phoneError.className = 'error-message';
    phoneError.style.display = 'none';
    phoneError.style.color = 'red';
    phoneError.style.fontSize = '0.8rem';
    phoneError.style.marginTop = '5px';

    // Insert error message elements after their respective inputs
    nameInput.parentNode.insertBefore(nameError, nameInput.nextSibling);
    emailInput.parentNode.insertBefore(emailError, emailInput.nextSibling);
    phoneInput.parentNode.parentNode.insertBefore(phoneError, phoneInput.parentNode.nextSibling);

    // Validation function for the name field
    function validateName() {
        const nameValue = nameInput.value.trim();
        const nameRegex = /^[A-Za-z\u00C0-\u017F\s]{3,}$/; // Letters only (including accented), min 3 chars

        if (!nameRegex.test(nameValue)) {
            nameInput.classList.add('invalid-input');
            nameError.style.display = 'block';
            nameError.textContent = 'Name must contain only letters and be at least 3 characters long';
            return false;
        } else {
            nameInput.classList.remove('invalid-input');
            nameError.style.display = 'none';
            return true;
        }
    }
    
    // Validation function for the email field
    function validateEmail() {
        const emailValue = emailInput.value.trim();
        // RFC 5322 compliant email regex
        const emailRegex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

        if (!emailRegex.test(emailValue)) {
            emailInput.classList.add('invalid-input');
            emailError.style.display = 'block';
            emailError.textContent = 'Please enter a valid email address';
            return false;
        } else {
            emailInput.classList.remove('invalid-input');
            emailError.style.display = 'none';
            return true;
        }
    }
    
    // Validation function for the phone field
    function validatePhone() {
        const phoneValue = '0' + phoneInput.value.trim();
        // Bulgarian phone format: 10 digits starting with 0
        const phoneRegex = /^0[0-9]{9}$/;
        
        if (!phoneRegex.test(phoneValue)) {
            phoneInput.classList.add('invalid-input');
            phoneError.style.display = 'block';
            phoneError.textContent = 'Please enter a valid phone number (9 digits after the leading 0)';
            return false;
        } else {
            phoneInput.classList.remove('invalid-input');
            phoneError.style.display = 'none';
            return true;
        }
    }

    // Format phone input to ensure correct format
    phoneInput.addEventListener('input', function(e) {
        // Remove non-digit characters
        let value = e.target.value.replace(/\D/g, '');
        
        // Add leading zero if missing
        if (value && value.charAt(0) !== '0') {
            value = '0' + value;
        }
        
        // Limit to 10 digits
        if (value.length > 10) {
            value = value.substring(0, 10);
        }
        
        // Display without the leading zero in the input field, since we show it separately
        let displayValue = value;
        if (value.startsWith('0') && value.length > 1) {
            displayValue = value.substring(1);
        }
        
        // Update input value
        e.target.value = displayValue;
    });

    // Live validation as user types
    nameInput.addEventListener('input', validateName);
    nameInput.addEventListener('blur', validateName);
    
    emailInput.addEventListener('input', validateEmail);
    emailInput.addEventListener('blur', validateEmail);
    
    phoneInput.addEventListener('input', validatePhone);
    phoneInput.addEventListener('blur', validatePhone);

    // Form submission validation
    form.addEventListener('submit', function(event) {
        let valid = true;
        const requiredFields = form.querySelectorAll('[required]');

        // Validate name, email, and phone first
        if (!validateName()) {
            valid = false;
        }
        
        if (!validateEmail()) {
            valid = false;
        }
        
        if (!validatePhone()) {
            valid = false;
        }
        
        // Prepend country code to phone number in a hidden field
        if (valid && phoneInput.value) {
            // Get the original form data
            const formData = new FormData(form);
            
            // Create a hidden input for the full phone number
            const hiddenPhoneInput = document.createElement('input');
            hiddenPhoneInput.type = 'hidden';
            hiddenPhoneInput.name = 'full_phone';
            hiddenPhoneInput.value = '+359' + phoneInput.value; // Add country code to the digits after (0)
            form.appendChild(hiddenPhoneInput);
        }

        // Validate other required fields
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                valid = false;
                field.classList.add('error');
            } else {
                field.classList.remove('error');
            }
        });

        if (!valid) {
            event.preventDefault();
            alert('Please correct all errors before submitting the form.');
        }
    });
});