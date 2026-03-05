// API Base URL - Using relative URL for compatibility
const API_BASE_URL = window.API_BASE_URL || '/api';

// Check admin authentication
const adminToken = localStorage.getItem('adminToken');

if (!adminToken) {
    window.location.href = 'admin_login.html';
}

// Logout handler
const logoutBtn = document.getElementById('logoutBtn');
logoutBtn.addEventListener('click', () => {
    localStorage.removeItem('adminToken');
    localStorage.removeItem('adminData');
    window.location.href = '../index.html';
});

// Load dashboard data
async function loadDashboard() {
    try {
        const response = await fetch(`${API_BASE_URL}/admin/dashboard`, {
            headers: {
                'Authorization': `Bearer ${adminToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayDashboard(data.dashboard);
        } else {
            showError(data.message);
        }
    } catch (error) {
        showError('Failed to load dashboard data.');
    }
}

// Display dashboard data
function displayDashboard(dashboard) {
    // Update statistics
    document.getElementById('totalStudents').textContent = dashboard.total_students;
    document.getElementById('totalEvents').textContent = dashboard.total_events;
    document.getElementById('unauthorizedScans').textContent = dashboard.unauthorized_scans;
    
    // Display event registrations
    displayEventRegistrations(dashboard.event_registrations);
    
    // Display department statistics
    displayDepartmentStats(dashboard.department_stats);
    
    // Populate event selects
    populateEventSelects(dashboard.event_registrations);
}

// Display event registrations
function displayEventRegistrations(events) {
    const container = document.getElementById('eventRegistrations');
    
    if (events.length === 0) {
        container.innerHTML = '<p>No event registrations found.</p>';
        return;
    }
    
    container.innerHTML = `
        <table>
            <thead>
                <tr>
                    <th>Event Name</th>
                    <th>Registered</th>
                    <th>Attended</th>
                    <th>Attendance %</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                ${events.map(event => `
                    <tr>
                        <td>${event.event_name}</td>
                        <td>${event.total_registered}</td>
                        <td>${event.total_attended}</td>
                        <td>${event.attendance_percentage}%</td>
                        <td>
                            <button class="btn btn-sm btn-primary" onclick="viewEventReport('${event.event_id}', '${event.event_name}')">View Report</button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

// Display department statistics
function displayDepartmentStats(stats) {
    const container = document.getElementById('departmentStats');
    
    if (stats.length === 0) {
        container.innerHTML = '<p>No department statistics available.</p>';
        return;
    }
    
    container.innerHTML = stats.map(stat => `
        <div class="stat-item">
            <span>${stat.department}</span>
            <strong>${stat.count}</strong>
        </div>
    `).join('');
}

// Populate event select dropdowns
function populateEventSelects(events) {
    const eventSelect = document.getElementById('eventSelect');
    const reportEventSelect = document.getElementById('reportEventSelect');
    
    events.forEach(event => {
        const option = new Option(event.event_name, event.event_id);
        eventSelect.add(option.cloneNode(true));
        reportEventSelect.add(option);
    });
}

// Generate QR Code
const generateQRBtn = document.getElementById('generateQRBtn');
generateQRBtn.addEventListener('click', async () => {
    const eventId = document.getElementById('eventSelect').value;
    
    if (!eventId) {
        showError('Please select an event');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/admin/generate-qr/${eventId}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${adminToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayQRCode(data.qr_code, data.event_name);
            showSuccess('QR Code generated successfully!');
        } else {
            showError(data.message);
        }
    } catch (error) {
        showError('Failed to generate QR code.');
    }
});

// Display QR Code
function displayQRCode(qrImage, eventName) {
    const qrDisplay = document.getElementById('qrCodeDisplay');
    const qrEventName = document.getElementById('qrEventName');
    const qrCodeImage = document.getElementById('qrCodeImage');
    
    qrEventName.textContent = eventName;
    qrCodeImage.src = qrImage;
    qrDisplay.style.display = 'block';
    
    // Download QR Code
    document.getElementById('downloadQRBtn').onclick = () => {
        const link = document.createElement('a');
        link.href = qrImage;
        link.download = `QR_${eventName.replace(/ /g, '_')}.png`;
        link.click();
    };
}

// View Report
const viewReportBtn = document.getElementById('viewReportBtn');
viewReportBtn.addEventListener('click', async () => {
    const eventId = document.getElementById('reportEventSelect').value;
    
    if (!eventId) {
        showError('Please select an event');
        return;
    }
    
    const eventName = document.getElementById('reportEventSelect').selectedOptions[0].text;
    await viewEventReport(eventId, eventName);
});

// View Event Report
async function viewEventReport(eventId, eventName) {
    try {
        const response = await fetch(`${API_BASE_URL}/admin/attendance-report/${eventId}`, {
            headers: {
                'Authorization': `Bearer ${adminToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayAttendanceReport(data, eventName);
        } else {
            showError(data.message);
        }
    } catch (error) {
        showError('Failed to load attendance report.');
    }
}

// Display Attendance Report
function displayAttendanceReport(data, eventName) {
    const reportContainer = document.getElementById('attendanceReport');
    
    reportContainer.innerHTML = `
        <h3>${eventName} - Attendance Report</h3>
        <div class="report-summary">
            <div class="report-stat">
                <h4>${data.total_registered}</h4>
                <p>Registered</p>
            </div>
            <div class="report-stat">
                <h4>${data.total_attended}</h4>
                <p>Present</p>
            </div>
            <div class="report-stat">
                <h4>${data.total_absent}</h4>
                <p>Absent</p>
            </div>
            <div class="report-stat">
                <h4>${data.attendance_percentage}%</h4>
                <p>Attendance</p>
            </div>
        </div>
        
        ${data.student_list && data.student_list.length > 0 ? `
            <table class="attendance-table">
                <thead>
                    <tr>
                        <th>S.No</th>
                        <th>Register Number</th>
                        <th>Name</th>
                        <th>Department</th>
                        <th>Course</th>
                        <th>Year</th>
                        <th>Status</th>
                        <th>Time</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.student_list.map((record, index) => `
                        <tr class="${record.status === 'Present' ? 'status-present' : 'status-absent'}">
                            <td>${index + 1}</td>
                            <td>${record.register_number}</td>
                            <td>${record.student_name}</td>
                            <td>${record.department}</td>
                            <td>${record.course || 'N/A'}</td>
                            <td>${record.year}</td>
                            <td>
                                <span class="status-badge ${record.status === 'Present' ? 'badge-present' : 'badge-absent'}">
                                    ${record.status === 'Present' ? '✓ Present' : '✗ Absent'}
                                </span>
                            </td>
                            <td>${record.marked_at ? new Date(record.marked_at).toLocaleString() : '-'}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        ` : '<p class="no-data">No students registered for this event.</p>'}
    `;
    
    reportContainer.style.display = 'block';
}

// Export to Excel
const exportExcelBtn = document.getElementById('exportExcelBtn');
exportExcelBtn.addEventListener('click', async () => {
    const eventId = document.getElementById('reportEventSelect').value;
    
    if (!eventId) {
        showError('Please select an event');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/admin/export-attendance/${eventId}`, {
            headers: {
                'Authorization': `Bearer ${adminToken}`
            }
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `attendance_report_${Date.now()}.xlsx`;
            a.click();
            window.URL.revokeObjectURL(url);
            
            showSuccess('Report exported successfully!');
        } else {
            showError('Failed to export report.');
        }
    } catch (error) {
        showError('Failed to export report.');
    }
});

// Search Student
const searchBtn = document.getElementById('searchBtn');
searchBtn.addEventListener('click', async () => {
    const registerNumber = document.getElementById('searchRegNumber').value.trim();
    
    if (!registerNumber) {
        showError('Please enter a register number');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/student/search/${registerNumber}`, {
            headers: {
                'Authorization': `Bearer ${adminToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            displaySearchResult(data.student);
        } else {
            showError(data.message);
        }
    } catch (error) {
        showError('Search failed. Please try again.');
    }
});

// Display Search Result
function displaySearchResult(student) {
    const searchResult = document.getElementById('searchResult');
    
    searchResult.innerHTML = `
        <h3>Student Details</h3>
        <p><strong>Name:</strong> ${student.name}</p>
        <p><strong>Register Number:</strong> ${student.register_number}</p>
        <p><strong>Department:</strong> ${student.department}</p>
        <p><strong>Course/Programme:</strong> ${student.course || 'N/A'}</p>
        <p><strong>Year:</strong> ${student.year}</p>
        <p><strong>Email:</strong> ${student.email}</p>
        <p><strong>Phone:</strong> ${student.phone_number}</p>
        <p><strong>Registered Events:</strong></p>
        <ul>
            ${student.registered_events && student.registered_events.length > 0 
                ? student.registered_events.map(event => `<li>${event.event_name}</li>`).join('') 
                : '<li>No registered events</li>'}
        </ul>
    `;
    
    searchResult.style.display = 'block';
}

// View Unauthorized Logs
const viewLogsBtn = document.getElementById('viewLogsBtn');
viewLogsBtn.addEventListener('click', async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/admin/unauthorized-logs`, {
            headers: {
                'Authorization': `Bearer ${adminToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayUnauthorizedLogs(data.logs);
        } else {
            showError(data.message);
        }
    } catch (error) {
        showError('Failed to load logs.');
    }
});

// Display Unauthorized Logs
function displayUnauthorizedLogs(logs) {
    const logsContainer = document.getElementById('unauthorizedLogs');
    
    if (logs.length === 0) {
        logsContainer.innerHTML = '<p>No unauthorized scan attempts found.</p>';
    } else {
        logsContainer.innerHTML = logs.map(log => `
            <div class="log-item">
                <p><strong>Time:</strong> ${new Date(log.scanned_at).toLocaleString()}</p>
                <p><strong>IP Address:</strong> ${log.ip_address}</p>
                <p><strong>Details:</strong> ${JSON.stringify(log.scan_data)}</p>
            </div>
        `).join('');
    }
    
    logsContainer.style.display = 'block';
}

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

// Load dashboard on page load
loadDashboard();
