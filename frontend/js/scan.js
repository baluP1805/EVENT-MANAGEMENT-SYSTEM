// API Base URL - can be overridden at deploy time via `window.__API_BASE_URL__`
const API_BASE_URL = window.API_BASE_URL || 'http://localhost:5000/api';

// Check authentication
const token = localStorage.getItem('token');
const studentData = JSON.parse(localStorage.getItem('studentData'));

if (!token || !studentData) {
    window.location.href = 'login.html';
}

// Display student name
const studentNameEl = document.getElementById('studentName');
if (studentNameEl) {
    studentNameEl.textContent = studentData.name;
}

// Logout handler
const logoutBtn = document.getElementById('logoutBtn');
if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('token');
        localStorage.removeItem('studentData');
        localStorage.removeItem('registeredEvents');
        window.location.href = '../index.html';
    });
}

// Camera scanning setup using html5-qrcode
let html5QrCode = null;
let currentCameraId = null;
let torchOn = false;

async function listCameras() {
    try {
        // Check if library is loaded
        if (typeof Html5Qrcode === 'undefined') {
            console.error('Html5Qrcode library not loaded');
            return;
        }
        
        const devices = await Html5Qrcode.getCameras();
        const select = document.getElementById('cameraSelect');
        select.innerHTML = '';
        
        if (!devices || devices.length === 0) {
            console.warn('No cameras available');
            return;
        }
        
        devices.forEach(cam => {
            const opt = document.createElement('option');
            // Handle different property names for camera ID
            const cameraId = cam.id || cam.deviceId || (typeof cam === 'string' ? cam : '');
            const label = cam.label || cameraId || 'Unknown Camera';
            opt.value = cameraId;
            opt.textContent = label;
            select.appendChild(opt);
        });
        
        if (devices.length > 0) {
            const firstCamera = devices[0];
            currentCameraId = firstCamera.id || firstCamera.deviceId || (typeof firstCamera === 'string' ? firstCamera : '');
            select.value = currentCameraId;
            console.log('Camera selected:', currentCameraId);
        }
    } catch (e) {
        console.warn('No cameras available or permission denied', e);
    }
}

function onScanSuccess(decodedText, decodedResult) {
    // Place scanned content in textarea and auto-submit (without removing user's clipboard)
    const qrField = document.getElementById('qrData');
    qrField.value = decodedText;
    // stop scanning after successful decode to avoid duplicates
    stopScanner();
    // Trigger mark attendance automatically
    markAttendance(decodedText);
}

function onScanFailure(error) {
    // Log scan failures every 5 seconds for debugging
    if (!window.lastScanError || Date.now() - window.lastScanError > 5000) {
        console.log('[QR Scanner] Scan attempt:', error);
        window.lastScanError = Date.now();
    }
}

async function startScanner(cameraId) {
    // Check if library is loaded
    if (typeof Html5Qrcode === 'undefined') {
        showError('QR Scanner library failed to load. Please refresh the page and try again.');
        return;
    }
    
    // Validate camera ID
    if (!cameraId) {
        console.warn('No valid camera ID provided');
        showError('No valid camera found. Please select a camera from the dropdown.');
        return;
    }
    
    const qrRegionId = 'qr-reader';
    
    // Stop scanner if already running
    if (html5QrCode) {
        try {
            await html5QrCode.stop();
            await html5QrCode.clear();
        } catch (e) { /* ignore */ }
    }
    
    // Create fresh instance
    html5QrCode = new Html5Qrcode(qrRegionId, { experimentalFeatures: { useBarCodeDetectorIfSupported: true } });
    
    try {
        console.log('Starting scanner with camera ID:', cameraId);
        const config = { fps: 20, qrbox: { width: 300, height: 300 }, aspectRatio: 1.0 };
        await html5QrCode.start(cameraId, config, onScanSuccess, onScanFailure);
        document.getElementById('startScanBtn').style.display = 'none';
        document.getElementById('stopScanBtn').style.display = '';
        document.getElementById('toggleTorchBtn').style.display = '';
    } catch (e) {
        console.error('Failed to start scanner', e);
        const errorMsg = e?.message || e?.toString() || 'Camera access failed';
        showError(`Failed to access camera: ${errorMsg}. Please allow camera permission or paste QR data manually.`);
    }
}

async function stopScanner() {
    if (html5QrCode) {
        try { await html5QrCode.stop(); } catch (e) { /* ignore */ }
        html5QrCode.clear();
    }
    document.getElementById('startScanBtn').style.display = '';
    document.getElementById('stopScanBtn').style.display = 'none';
    document.getElementById('toggleTorchBtn').style.display = 'none';
}

async function toggleTorch() {
    if (!html5QrCode) return;
    try {
        torchOn = !torchOn;
        await html5QrCode.applyVideoConstraints({ advanced: [{ torch: torchOn }] });
    } catch (e) {
        console.warn('Torch not supported on this device', e);
        showNotification('Torch not supported on this device', 'info', 2500);
    }
}

async function markAttendance(qrData) {
    const qrDataTrim = (qrData || document.getElementById('qrData').value).trim();
    if (!qrDataTrim) {
        showError('Please paste the QR code data');
        return;
    }
    try {
        const response = await fetch(`${API_BASE_URL}/attendance/scan`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ qr_data: qrDataTrim })
        });
        const data = await response.json();
        if (data.success) {
            showSuccess(data.message);
            displayAttendanceResult(data);
            document.getElementById('qrData').value = '';
        } else {
            showError(data.message);
        }
    } catch (error) {
        showError('Failed to mark attendance. Please try again.');
    }
}

// Wire up camera controls
document.getElementById('startScanBtn').addEventListener('click', async () => {
    const select = document.getElementById('cameraSelect');
    currentCameraId = select.value;
    await startScanner(currentCameraId);
});

document.getElementById('stopScanBtn').addEventListener('click', async () => {
    await stopScanner();
});

document.getElementById('toggleTorchBtn').addEventListener('click', async () => {
    await toggleTorch();
});

document.getElementById('cameraSelect').addEventListener('change', async (e) => {
    currentCameraId = e.target.value;
    if (document.getElementById('stopScanBtn').style.display !== 'none') {
        await stopScanner();
        await startScanner(currentCameraId);
    }
});

// Initialize camera list on page load
listCameras();

// Keep the original manual mark button behavior for fallback
const markAttendanceBtn = document.getElementById('markAttendanceBtn');
markAttendanceBtn.addEventListener('click', async () => {
    await markAttendance();
});

// Display attendance result
function displayAttendanceResult(data) {
    const resultBox = document.getElementById('attendanceResult');
    resultBox.innerHTML = `
        <div style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">✓</div>
            <h2 style="color: var(--success-color); margin-bottom: 1rem;">Attendance Marked!</h2>
            <p><strong>Event:</strong> ${data.event_name}</p>
            <p><strong>Student:</strong> ${data.student_name}</p>
            <p style="margin-top: 1rem; color: var(--text-secondary);">
                📧 A confirmation email has been sent to your registered email address.
            </p>
        </div>
    `;
    resultBox.style.display = 'block';
}

// View My Attendance
const viewMyAttendanceBtn = document.getElementById('viewMyAttendanceBtn');
viewMyAttendanceBtn.addEventListener('click', async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/attendance/my-attendance?student_id=${studentData.id}`);
        const data = await response.json();
        
        if (data.success) {
            displayMyAttendance(data.attendance, data.total_attended);
        } else {
            showError(data.message);
        }
    } catch (error) {
        showError('Failed to load attendance records.');
    }
});

// Display my attendance
function displayMyAttendance(attendance, totalAttended) {
    const myAttendanceList = document.getElementById('myAttendanceList');
    myAttendanceList.innerHTML = '';
    
    if (attendance.length === 0) {
        myAttendanceList.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">No attendance records found.</p>';
    } else {
        myAttendanceList.innerHTML = `
            <p style="margin-bottom: 1rem;"><strong>Total Events Attended: ${totalAttended}</strong></p>
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr>
                        <th style="padding: 0.75rem; text-align: left; border-bottom: 2px solid var(--border-color);">Event</th>
                        <th style="padding: 0.75rem; text-align: left; border-bottom: 2px solid var(--border-color);">Date & Time</th>
                        <th style="padding: 0.75rem; text-align: left; border-bottom: 2px solid var(--border-color);">Status</th>
                    </tr>
                </thead>
                <tbody>
                    ${attendance.map(record => `
                        <tr>
                            <td style="padding: 0.75rem; border-bottom: 1px solid var(--border-color);">${record.event_name}</td>
                            <td style="padding: 0.75rem; border-bottom: 1px solid var(--border-color);">${new Date(record.marked_at).toLocaleString()}</td>
                            <td style="padding: 0.75rem; border-bottom: 1px solid var(--border-color);">
                                <span style="background: var(--success-color); color: white; padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.85rem;">
                                    ${record.status}
                                </span>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }
    
    myAttendanceList.style.display = 'block';
});

// Helper functions
function showError(message) {
    const errorMessage = document.getElementById('errorMessage');
    const successMessage = document.getElementById('successMessage');
    
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    successMessage.style.display = 'none';
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showSuccess(message) {
    const errorMessage = document.getElementById('errorMessage');
    const successMessage = document.getElementById('successMessage');
    
    successMessage.textContent = message;
    successMessage.style.display = 'block';
    errorMessage.style.display = 'none';
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
