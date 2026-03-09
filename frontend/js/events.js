// API Base URL - Using relative URL for compatibility
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

// Profile button handler
const profileBtn = document.getElementById('profileBtn');
if (profileBtn) {
    profileBtn.addEventListener('click', showProfile);
}

// QR Scanner button handler
const scanQRBtn = document.getElementById('scanQRBtn');
if (scanQRBtn) {
    scanQRBtn.addEventListener('click', openQRScanner);
}

// Check if student is already registered
async function checkRegistrationStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/student/my-events`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        const data = await response.json();
        
        if (data.success && data.events.length > 0) {
            // Student is already registered
            document.getElementById('registrationForm').style.display = 'none';
            document.getElementById('registeredEventView').style.display = 'block';
            document.getElementById('registrationStatusBadge').style.display = 'block';
            displayRegisteredEvent(data.events[0]);
            return true;
        }
        return false;
    } catch (error) {
        console.error('Failed to check registration status:', error);
        return false;
    }
}

// Display registered event
function displayRegisteredEvent(event) {
    const eventCard = document.getElementById('registeredEventCard');
    eventCard.innerHTML = `
        <div class="event-card-large">
            <div class="event-icon">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
            </div>
            <h2>${event.event_name}</h2>
            <p class="event-description">${event.description}</p>
            <div class="event-meta-large">
                <div class="meta-item">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                        <line x1="16" y1="2" x2="16" y2="6"></line>
                        <line x1="8" y1="2" x2="8" y2="6"></line>
                        <line x1="3" y1="10" x2="21" y2="10"></line>
                    </svg>
                    <span>${event.date}</span>
                </div>
                <div class="meta-item">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                        <circle cx="12" cy="10" r="3"></circle>
                    </svg>
                    <span>${event.venue}</span>
                </div>
            </div>
            <div class="event-actions">
                <button class="btn btn-primary" onclick="openQRScanner()">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                    </svg>
                    Scan QR to Mark Attendance
                </button>
            </div>
        </div>
    `;
}

// Load events
async function loadEvents() {
    try {
        // First check if already registered
        const isRegistered = await checkRegistrationStatus();
        if (isRegistered) {
            return;
        }

        const response = await fetch(`${API_BASE_URL}/student/events`);
        const data = await response.json();
        
        if (data.success) {
            displayEvents(data.events);
        } else {
            showError('Failed to load events');
        }
    } catch (error) {
        console.error('Error loading events:', error);
        showError('Failed to load events. Please try again.');
    }
}

// Display events
function displayEvents(events) {
    const eventsGrid = document.getElementById('eventsGrid');
    eventsGrid.innerHTML = '';
    
    if (!events || events.length === 0) {
        eventsGrid.innerHTML = '<p style="text-align: center; color: var(--text-secondary); padding: 2rem;">No events available at the moment.</p>';
        return;
    }
    
    events.forEach(event => {
        const eventCard = document.createElement('div');
        eventCard.className = 'event-card-enhanced';
        
        eventCard.innerHTML = `
            <label class="event-label">
                <input type="radio" name="event" value="${event.id}" data-name="${event.event_name}">
                <div class="event-content">
                    <div class="event-header">
                        <h3 class="event-title">${event.event_name}</h3>
                        <div class="radio-checkmark"></div>
                    </div>
                    <p class="event-description">${event.description}</p>
                    <div class="event-meta-enhanced">
                        <div class="meta-item">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                                <line x1="16" y1="2" x2="16" y2="6"></line>
                                <line x1="8" y1="2" x2="8" y2="6"></line>
                                <line x1="3" y1="10" x2="21" y2="10"></line>
                            </svg>
                            <span>${event.date}</span>
                        </div>
                        <div class="meta-item">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                                <circle cx="12" cy="10" r="3"></circle>
                            </svg>
                            <span>${event.venue}</span>
                        </div>
                    </div>
                </div>
            </label>
        `;
        
        // Toggle selected class on click
        const radio = eventCard.querySelector('input[type="radio"]');
        radio.addEventListener('change', () => {
            // Remove selected class from all cards
            document.querySelectorAll('.event-card-enhanced').forEach(card => {
                card.classList.remove('selected');
            });
            // Add selected class to this card
            if (radio.checked) {
                eventCard.classList.add('selected');
            }
        });
        
        eventsGrid.appendChild(eventCard);
    });
}

// Event form submission
const eventForm = document.getElementById('eventForm');
eventForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const selectedRadio = document.querySelector('input[name="event"]:checked');
    
    if (!selectedRadio) {
        showError('Please select an event');
        return;
    }
    
    const eventId = selectedRadio.value;
    const eventName = selectedRadio.dataset.name;
    
    try {
        const response = await fetch(`${API_BASE_URL}/student/register-events`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ event_ids: [eventId] })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Store registered event
            localStorage.setItem('registeredEvents', JSON.stringify([eventName]));
            
            showSuccess(data.message);
            
            // Redirect to success page
            setTimeout(() => {
                window.location.href = 'success.html';
            }, 1500);
        } else {
            showError(data.message);
        }
    } catch (error) {
        console.error('Registration error:', error);
        showError('Registration failed. Please try again.');
    }
});

// Profile Modal
async function showProfile() {
    try {
        const response = await fetch(`${API_BASE_URL}/student/profile`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        const data = await response.json();
        
        if (data.success) {
            const student = data.student;
            const profileData = document.getElementById('profileData');
            profileData.innerHTML = `
                <div class="profile-item">
                    <label>Name</label>
                    <div class="profile-value">${student.name}</div>
                </div>
                <div class="profile-item">
                    <label>Register Number</label>
                    <div class="profile-value">${student.register_number}</div>
                </div>
                <div class="profile-item">
                    <label>Department</label>
                    <div class="profile-value">${student.department}</div>
                </div>
                <div class="profile-item">
                    <label>Course/Programme</label>
                    <div class="profile-value">${student.course || 'N/A'}</div>
                </div>
                <div class="profile-item">
                    <label>Year</label>
                    <div class="profile-value">${student.year}</div>
                </div>
                <div class="profile-item">
                    <label>Email</label>
                    <div class="profile-value">${student.email}</div>
                </div>
                <div class="profile-item">
                    <label>Phone Number</label>
                    <div class="profile-value">${student.phone_number}</div>
                </div>
                <div class="profile-item">
                    <label>Registered Events</label>
                    <div class="profile-value">${student.registered_events_count}</div>
                </div>
            `;
            document.getElementById('profileModal').style.display = 'flex';
        }
    } catch (error) {
        console.error('Profile error:', error);
        showError('Failed to load profile');
    }
}

// Close profile modal
document.querySelector('.close-modal')?.addEventListener('click', () => {
    document.getElementById('profileModal').style.display = 'none';
});

// QR Scanner functionality
let html5QrCodeModal = null;
let isModalScanning = false;

async function openQRScanner() {
    // Check if library is loaded
    if (typeof Html5Qrcode === 'undefined') {
        alert('QR Scanner library failed to load. Please refresh the page and try again.');
        console.error('Html5Qrcode is not defined. Library may not have loaded from CDN.');
        return;
    }
    
    // Check if student is registered for an event
    const registeredEventView = document.getElementById('registeredEventView');
    if (!registeredEventView || registeredEventView.style.display === 'none') {
        alert('⚠️ Please register for an event first before scanning QR codes for attendance.');
        return;
    }
    
    const modal = document.getElementById('qrScannerModal');
    modal.style.display = 'flex';
    document.getElementById('scanStatus').innerHTML = `
        <span style="color: #3b82f6;">🔍 Initializing camera...</span>
    `;
    
    try {
        // Stop existing scanner if running
        if (isModalScanning && html5QrCodeModal) {
            await stopModalScanning();
            await new Promise(resolve => setTimeout(resolve, 300)); // Wait for cleanup
        }
        
        // Initialize html5QrCode if not already done
        if (!html5QrCodeModal) {
            html5QrCodeModal = new Html5Qrcode('qr-reader-modal', {
                experimentalFeatures: {
                    useBarCodeDetectorIfSupported: true
                }
            });
        }
        
        // Get cameras
        const devices = await Html5Qrcode.getCameras();
        
        if (devices.length === 0) {
            document.getElementById('scanStatus').innerHTML = `
                <span style="color: #ef4444; font-weight: 600;">❌ No camera found</span><br>
                <small style="color: #6b7280;">Please check camera permissions in browser settings</small>
            `;
            return;
        }
        
        // Prefer back/environment camera on mobile
        let cameraId = devices[devices.length - 1].id;
        
        // Look for environment/back camera
        const backCamera = devices.find(device => 
            device.label.toLowerCase().includes('back') || 
            device.label.toLowerCase().includes('environment')
        );
        
        if (backCamera) {
            cameraId = backCamera.id;
            console.log('Using back camera:', backCamera.label);
        } else {
            console.log('Using default camera:', devices[devices.length - 1].label || cameraId);
        }
        
        // Start scanning
        await startModalScanning(cameraId);
        
    } catch (error) {
        console.error('Camera error:', error);
        const errorMsg = error?.message || error?.toString() || 'Unknown error';
        document.getElementById('scanStatus').innerHTML = `
            <span style="color: #ef4444; font-weight: 600;">❌ Failed to access camera</span><br>
            <small style="color: #6b7280;">${errorMsg}</small><br>
            <small style="color: #6b7280;">Please allow camera permissions and try again</small>
        `;
    }
}

async function startModalScanning(cameraId) {
    try {
        const config = {
            fps: 20,  // Increased for faster detection
            qrbox: { width: 300, height: 300 },  // Larger scan area
            aspectRatio: 1.0,
            disableFlip: false  // Allow camera flip for better scanning
        };
        
        await html5QrCodeModal.start(
            cameraId,
            config,
            onModalScanSuccess,
            onModalScanFailure
        );
        
        isModalScanning = true;
        document.getElementById('scanStatus').innerHTML = `
            <span style="color: #10b981; font-weight: 600;">📷 Camera Active</span><br>
            <small style="color: #6b7280;">Position QR code within the green frame</small>
        `;
        
    } catch (error) {
        console.error('Scanning error:', error);
        const errorMsg = error?.message || error?.toString() || 'Unknown error';
        document.getElementById('scanStatus').innerHTML = `
            <span style="color: #ef4444; font-weight: 600;">❌ Scanning failed</span><br>
            <small style="color: #6b7280;">${errorMsg}</small>
        `;
    }
}

async function onModalScanSuccess(decodedText, decodedResult) {
    // Stop only the camera — keep modal open so the user can see the results
    await stopCameraKeepModal();
    
    // Show processing state inside the still-visible modal
    document.getElementById('scanStatus').innerHTML = `
        <span style="color: #3b82f6; font-weight: 600;">📱 QR Code detected! Verifying...</span>
    `;
    
    await processQRCode(decodedText);
}

function onModalScanFailure(error) {
    // Log scan failures every 5 seconds for debugging
    if (!window.lastModalScanError || Date.now() - window.lastModalScanError > 5000) {
        console.log('[QR Scanner] Scan attempt:', error);
        window.lastModalScanError = Date.now();
    }
}

async function processQRCode(qrData) {
    try {
        // Try to parse as JSON
        const qrJson = JSON.parse(qrData);
        
        // Validate QR code type (optional - backend will also validate)
        if (qrJson.type !== 'COLLEGE_EMS_EVENT') {
            document.getElementById('scanStatus').innerHTML = `
                <span style="color: #ef4444; font-weight: 600;">
                    ✗ Invalid QR code. Not a College EMS event QR.
                </span>
            `;
            setTimeout(() => {
                stopModalScanning();
            }, 2000);
            return;
        }
        
        // Show event info from QR code
        document.getElementById('scanStatus').innerHTML = `
            <span style="color: #3b82f6; font-weight: 600;">
                📱 Event: ${qrJson.event_name || 'Unknown'}<br>
                ⏳ Marking attendance...
            </span>
        `;
        
        // Send to backend
        const response = await fetch(`${API_BASE_URL}/attendance/scan`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ qr_data: qrData })
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('scanStatus').innerHTML = `
                <div style="background:#d1fae5; border:2px solid #10b981; border-radius:12px; padding:1.25rem; text-align:center;">
                    <div style="font-size:2.5rem; margin-bottom:0.5rem;">✅</div>
                    <div style="color:#065f46; font-weight:700; font-size:1.15rem; margin-bottom:0.4rem;">Attendance Marked!</div>
                    <div style="color:#047857; font-size:0.95rem; margin-bottom:0.25rem;">📅 Event: <strong>${data.event_name}</strong></div>
                    <div style="color:#047857; font-size:0.9rem;">👤 Student: <strong>${data.student_name}</strong></div>
                    <div style="color:#6b7280; font-size:0.8rem; margin-top:0.5rem;">Closing in a moment...</div>
                </div>
            `;
            setTimeout(() => {
                stopModalScanning();
                showSuccess(`Attendance marked for ${data.event_name}!`);
            }, 2800);
        } else {
            document.getElementById('scanStatus').innerHTML = `
                <div style="background:#fee2e2; border:2px solid #ef4444; border-radius:12px; padding:1.25rem; text-align:center;">
                    <div style="font-size:2rem; margin-bottom:0.5rem;">❌</div>
                    <div style="color:#991b1b; font-weight:700; font-size:1rem;">${data.message}</div>
                    <div style="color:#6b7280; font-size:0.8rem; margin-top:0.5rem;">Closing in a moment...</div>
                </div>
            `;
            setTimeout(() => stopModalScanning(), 3000);
        }
    } catch (error) {
        console.error('QR processing error:', error);
        const isJsonError = error instanceof SyntaxError;
        document.getElementById('scanStatus').innerHTML = `
            <div style="background:#fee2e2; border:2px solid #ef4444; border-radius:12px; padding:1.25rem; text-align:center;">
                <div style="font-size:2rem; margin-bottom:0.5rem;">❌</div>
                <div style="color:#991b1b; font-weight:700; font-size:1rem;">
                    ${isJsonError ? 'Invalid QR code — not a College EMS event code' : 'Failed to process QR code'}
                </div>
                <div style="color:#6b7280; font-size:0.8rem; margin-top:0.5rem;">Closing in a moment...</div>
            </div>
        `;
        setTimeout(() => stopModalScanning(), 2800);
    }
}

async function stopCameraKeepModal() {
    // Stop the camera stream only — modal stays open to show results
    if (html5QrCodeModal) {
        try {
            await html5QrCodeModal.stop();
            html5QrCodeModal.clear();
        } catch (e) {
            console.log('Scanner already stopped or not started');
        }
        html5QrCodeModal = null; // Force fresh instance on next open
        isModalScanning = false;
    }
}

async function stopModalScanning() {
    // Stop camera and close the modal entirely
    await stopCameraKeepModal();
    document.getElementById('qrScannerModal').style.display = 'none';
    document.getElementById('scanStatus').innerHTML = '🔍 Initializing camera...';
}

// Stop scan button
document.getElementById('stopModalScanBtn')?.addEventListener('click', async () => {
    await stopModalScanning();
});
document.querySelector('.close-scanner')?.addEventListener('click', async () => {
    await stopModalScanning();
});

// Close modals when clicking outside
window.addEventListener('click', async (event) => {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
        if (event.target.id === 'qrScannerModal') {
            await stopModalScanning();
        }
    }
});

// Helper functions
function showError(message) {
    const errorMessage = document.getElementById('errorMessage');
    const successMessage = document.getElementById('successMessage');
    
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    successMessage.style.display = 'none';
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showSuccess(message) {
    const errorMessage = document.getElementById('errorMessage');
    const successMessage = document.getElementById('successMessage');
    
    successMessage.textContent = message;
    successMessage.style.display = 'block';
    errorMessage.style.display = 'none';
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Load events on page load
loadEvents();
