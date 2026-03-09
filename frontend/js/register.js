// API Base URL - Using relative URL for compatibility
const API_BASE_URL = window.API_BASE_URL || 'http://localhost:5000/api';

// Course data based on departments
const coursesByDepartment = {
    'Management': [
        'B.B.A',
        'B.Com',
        'B.Com CA (Computer Applications)',
        'B.Com PA (Professional Accounting)',
        'M.Com CA (Computer Applications)',
        'MBA (AICTE Approved)',
        'Ph.D. Commerce'
    ],
    'Science': [
        'B.Sc. Computer Science',
        'B.C.A',
        'B.Sc. Artificial Intelligence & Machine Learning',
        'B.Sc. Mathematics',
        'B.Sc. Physics',
        'B.Sc. Fashion Technology & Costume Designing',
        'B.Sc. Hotel Management & Catering Science',
        'M.Sc. Computer Science',
        'M.Sc. Mathematics'
    ],
    'Arts': [
        'B.A. Tamil',
        'B.A. English',
        'B.A. Public Administration',
        'M.A. English'
    ]
};

// Department change handler
const departmentSelect = document.getElementById('department');
const courseSelect = document.getElementById('course');

departmentSelect.addEventListener('change', (e) => {
    const selectedDepartment = e.target.value;
    
    // Clear existing courses
    courseSelect.innerHTML = '<option value="">Select Course/Programme</option>';
    
    if (selectedDepartment && coursesByDepartment[selectedDepartment]) {
        // Enable course dropdown
        courseSelect.disabled = false;
        
        // Populate courses for selected department
        coursesByDepartment[selectedDepartment].forEach(course => {
            const option = document.createElement('option');
            option.value = course;
            option.textContent = course;
            courseSelect.appendChild(option);
        });
    } else {
        // Disable if no department selected
        courseSelect.disabled = true;
        courseSelect.innerHTML = '<option value="">Select Department First</option>';
    }
});

// Registration Form Handler
const registerForm = document.getElementById('registerForm');

registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('name').value,
        register_number: document.getElementById('register_number').value,
        department: document.getElementById('department').value,
        course: document.getElementById('course').value,
        year: document.getElementById('year').value,
        email: document.getElementById('email').value,
        phone_number: document.getElementById('phone_number').value,
        password: document.getElementById('password').value
    };
    
    const errorMessage = document.getElementById('errorMessage');
    const successMessage = document.getElementById('successMessage');
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            successMessage.textContent = data.message;
            successMessage.style.display = 'block';
            errorMessage.style.display = 'none';
            
            // Clear form
            registerForm.reset();
            
            // Redirect to login page after 2 seconds
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
        } else {
            errorMessage.textContent = data.message;
            errorMessage.style.display = 'block';
            successMessage.style.display = 'none';
        }
    } catch (error) {
        errorMessage.textContent = 'Registration failed. Please try again.';
        errorMessage.style.display = 'block';
        successMessage.style.display = 'none';
    }
});

// Phone number validation
const phoneInput = document.getElementById('phone_number');
phoneInput.addEventListener('input', (e) => {
    e.target.value = e.target.value.replace(/[^0-9]/g, '');
});
