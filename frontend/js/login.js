// API Base URL - Using relative URL for compatibility
const API_BASE_URL = window.API_BASE_URL || '/api';

// Login Form Handler
const loginForm = document.getElementById('loginForm');
const adminLoginForm = document.getElementById('adminLoginForm');

if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        const errorMessage = document.getElementById('errorMessage');
        const successMessage = document.getElementById('successMessage');
        
        try {
            const response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Store token and student data
                localStorage.setItem('token', data.token);
                localStorage.setItem('studentData', JSON.stringify(data.student));
                
                successMessage.textContent = data.message;
                successMessage.style.display = 'block';
                errorMessage.style.display = 'none';
                
                // Redirect to events page
                setTimeout(() => {
                    window.location.href = 'events.html';
                }, 1000);
            } else {
                errorMessage.textContent = data.message;
                errorMessage.style.display = 'block';
                successMessage.style.display = 'none';
            }
        } catch (error) {
            errorMessage.textContent = 'Login failed. Please try again.';
            errorMessage.style.display = 'block';
            successMessage.style.display = 'none';
        }
    });
}

// Admin Login Form Handler
if (adminLoginForm) {
    adminLoginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        const errorMessage = document.getElementById('errorMessage');
        const successMessage = document.getElementById('successMessage');
        
        try {
            const response = await fetch(`${API_BASE_URL}/auth/admin/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Store admin token
                localStorage.setItem('adminToken', data.token);
                localStorage.setItem('adminData', JSON.stringify(data.admin));
                
                successMessage.textContent = data.message;
                successMessage.style.display = 'block';
                errorMessage.style.display = 'none';
                
                // Redirect to admin dashboard
                setTimeout(() => {
                    window.location.href = 'admin_dashboard.html';
                }, 1000);
            } else {
                errorMessage.textContent = data.message;
                errorMessage.style.display = 'block';
                successMessage.style.display = 'none';
            }
        } catch (error) {
            errorMessage.textContent = 'Admin login failed. Please try again.';
            errorMessage.style.display = 'block';
            successMessage.style.display = 'none';
        }
    });
}
