// API Base URL - Using relative URL for compatibility
const API_BASE_URL = window.API_BASE_URL || 'http://localhost:5000/api';

// Login Form Handler
const loginForm = document.getElementById('loginForm');
const adminLoginForm = document.getElementById('adminLoginForm');

if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;

        const errorMessage = document.getElementById('errorMessage');
        const successMessage = document.getElementById('successMessage');

        // Helper to show error
        function showErr(msg) {
            errorMessage.textContent = msg;
            errorMessage.style.display = 'block';
            successMessage.style.display = 'none';
        }

        // --- Step 1: try student login ---
        try {
            const studentRes = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            const studentData = await studentRes.json();

            if (studentData.success) {
                localStorage.setItem('token', studentData.token);
                localStorage.setItem('studentData', JSON.stringify(studentData.student));
                successMessage.textContent = studentData.message;
                successMessage.style.display = 'block';
                errorMessage.style.display = 'none';
                setTimeout(() => { window.location.href = 'events.html'; }, 900);
                return;
            }

            // --- Step 2: student login failed — try admin login ---
            const adminRes = await fetch(`${API_BASE_URL}/auth/admin/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            const adminData = await adminRes.json();

            if (adminData.success) {
                localStorage.setItem('adminToken', adminData.token);
                localStorage.setItem('adminData', JSON.stringify(adminData.admin));
                successMessage.textContent = 'Admin login successful. Redirecting…';
                successMessage.style.display = 'block';
                errorMessage.style.display = 'none';
                setTimeout(() => { window.location.href = 'admin_dashboard.html'; }, 900);
                return;
            }

            // Both failed — show a generic error
            showErr('Invalid email or password.');

        } catch (error) {
            showErr('Login failed. Please check your connection and try again.');
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
