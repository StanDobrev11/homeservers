document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');

    form.addEventListener('submit', function (event) {
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
            alert(translations.requiredFields || 'Please fill out all required fields.');
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
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
            // Use the translated message from the translations object defined in the template
            nameError.textContent = translations.nameError || 'Name must contain only letters and be at least 3 characters long';
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
            // Use the translated message
            emailError.textContent = translations.emailError || 'Please enter a valid email address';
            return false;
        } else {
            emailInput.classList.remove('invalid-input');
            emailError.style.display = 'none';
            return true;
        }
    }

    // Validation function for the phone field
    function validatePhone() {
        const phoneValue = phoneInput.value.trim();
        // Bulgarian phone format: 9 digits after the leading 0 (which is shown separately in UI)
        const phoneRegex = /^[0-9]{9}$/;

        if (!phoneRegex.test(phoneValue)) {
            phoneInput.classList.add('invalid-input');
            phoneError.style.display = 'block';
            // Use the translated message
            phoneError.textContent = translations.phoneError || 'Please enter a valid phone number (9 digits after the leading 0)';
            return false;
        } else {
            phoneInput.classList.remove('invalid-input');
            phoneError.style.display = 'none';
            return true;
        }
    }

    // Format phone input to ensure correct format
    phoneInput.addEventListener('input', function (e) {
        // Remove non-digit characters
        let value = e.target.value.replace(/\D/g, '');

        // Limit to 9 digits (since the leading 0 is displayed separately in the UI)
        if (value.length > 9) {
            value = value.substring(0, 9);
        }

        // Update input value directly - we only need the 9 digits after the (0)
        e.target.value = value;
    });

    // Live validation as user types
    nameInput.addEventListener('input', validateName);
    nameInput.addEventListener('blur', validateName);

    emailInput.addEventListener('input', validateEmail);
    emailInput.addEventListener('blur', validateEmail);

    phoneInput.addEventListener('input', validatePhone);
    phoneInput.addEventListener('blur', validatePhone);

    // Form submission validation
    form.addEventListener('submit', function (event) {
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
            hiddenPhoneInput.value = '+359' + phoneInput.value; // Add country code to the 9 digits

            // Also add the full format with the leading 0
            const fullNumberInput = document.createElement('input');
            fullNumberInput.type = 'hidden';
            fullNumberInput.name = 'full_bg_number';
            fullNumberInput.value = '0' + phoneInput.value; // Add leading 0 to the 9 digits

            form.appendChild(hiddenPhoneInput);
            form.appendChild(fullNumberInput);

            console.log('Phone number formatted:', {
                enteredDigits: phoneInput.value,
                internationalFormat: '+359' + phoneInput.value,
                localFormat: '0' + phoneInput.value
            });
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
            alert(translations.validationErrors || 'Please correct all errors before submitting the form.');
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById("menu-toggle");
    const mainNav = document.getElementById("main-nav");
    const langSelector = document.getElementById("language-selector");

    toggleButton.addEventListener("click", function () {
        mainNav.classList.toggle("active");
        langSelector.classList.toggle("active");
    });
});