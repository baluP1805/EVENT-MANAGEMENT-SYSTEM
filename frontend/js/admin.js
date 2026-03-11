// API Base URL - Using relative URL for compatibility
const API_BASE_URL = window.API_BASE_URL || 'http://localhost:5000/api';

// Check admin authentication
const adminToken = localStorage.getItem('adminToken');

if (!adminToken) {
    window.location.href = 'login.html';
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
    // Animated stat counters
    countUpAnimation('totalStudents', dashboard.total_students);
    countUpAnimation('totalEvents', dashboard.total_events);
    countUpAnimation('unauthorizedScans', dashboard.unauthorized_scans);
    
    // Display event registrations
    displayEventRegistrations(dashboard.event_registrations);
    
    // Display department statistics
    displayDepartmentStats(dashboard.department_stats);
    
    // Populate event selects
    populateEventSelects(dashboard.event_registrations);

    // Render Chart.js charts
    initCharts(dashboard);
}

// Display event registrations
function displayEventRegistrations(events) {
    const container = document.getElementById('eventRegistrations');

    if (events.length === 0) {
        container.innerHTML = '<p>No event registrations found.</p>';
        return;
    }

    container.innerHTML = `
        <div style="display:flex;justify-content:flex-end;margin-bottom:0.75rem;">
            <button class="btn btn-secondary" onclick="exportAllAttendance()">📥 Export All Events</button>
        </div>
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

// Holds the last searched student for edit/delete operations
let _currentStudent = null;

// Display Search Result
function displaySearchResult(student) {
    _currentStudent = student;
    const searchResult = document.getElementById('searchResult');
    const studentId = student.id || student._id;

    searchResult.innerHTML = `
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;flex-wrap:wrap;gap:0.5rem;">
            <h3 style="margin:0;">Student Details</h3>
            <div style="display:flex;gap:0.5rem;">
                <button class="btn btn-sm btn-primary" onclick="editStudent()">✏️ Edit</button>
                <button class="btn btn-sm btn-danger" onclick="deleteStudent('${studentId}', '${student.register_number}')">🗑️ Delete</button>
            </div>
        </div>
        <div class="student-info-grid">
            <p><strong>Name:</strong> ${student.name}</p>
            <p><strong>Register Number:</strong> ${student.register_number}</p>
            <p><strong>Department:</strong> ${student.department}</p>
            <p><strong>Course/Programme:</strong> ${student.course || 'N/A'}</p>
            <p><strong>Year:</strong> ${student.year}</p>
            <p><strong>Email:</strong> ${student.email}</p>
            <p><strong>Phone:</strong> ${student.phone_number}</p>
        </div>
        <p style="margin-top:0.75rem;"><strong>Registered Events:</strong></p>
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
    if (typeof showToast === 'function') {
        showToast(message, 'error');
    } else {
        const errorMessage = document.getElementById('errorMessage');
        const successMessage = document.getElementById('successMessage');
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
        successMessage.style.display = 'none';
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

function showSuccess(message) {
    if (typeof showToast === 'function') {
        showToast(message, 'success');
    } else {
        const errorMessage = document.getElementById('errorMessage');
        const successMessage = document.getElementById('successMessage');
        successMessage.textContent = message;
        successMessage.style.display = 'block';
        errorMessage.style.display = 'none';
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

/* === STUDENT EDIT === */
function editStudent() {
    if (!_currentStudent) return;
    const s = _currentStudent;
    const studentId = s.id || s._id;
    const searchResult = document.getElementById('searchResult');

    searchResult.innerHTML = `
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
            <h3 style="margin:0;">Edit Student</h3>
        </div>
        <div class="student-edit-form">
            <div class="edit-form-grid">
                <div class="form-group">
                    <label>Name</label>
                    <input type="text" id="editName" class="form-control" value="${s.name || ''}">
                </div>
                <div class="form-group">
                    <label>Department</label>
                    <input type="text" id="editDepartment" class="form-control" value="${s.department || ''}">
                </div>
                <div class="form-group">
                    <label>Course / Programme</label>
                    <input type="text" id="editCourse" class="form-control" value="${s.course || ''}">
                </div>
                <div class="form-group">
                    <label>Year</label>
                    <input type="text" id="editYear" class="form-control" value="${s.year || ''}">
                </div>
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" id="editEmail" class="form-control" value="${s.email || ''}">
                </div>
                <div class="form-group">
                    <label>Phone Number</label>
                    <input type="text" id="editPhone" class="form-control" value="${s.phone_number || ''}">
                </div>
            </div>
            <div style="display:flex;gap:0.75rem;margin-top:1rem;">
                <button class="btn btn-primary" onclick="saveEditStudent('${studentId}')">💾 Save Changes</button>
                <button class="btn btn-secondary" onclick="displaySearchResult(_currentStudent)">✕ Cancel</button>
            </div>
        </div>
    `;
    searchResult.style.display = 'block';
}

async function saveEditStudent(studentId) {
    const payload = {
        name:         document.getElementById('editName').value.trim(),
        department:   document.getElementById('editDepartment').value.trim(),
        course:       document.getElementById('editCourse').value.trim(),
        year:         document.getElementById('editYear').value.trim(),
        email:        document.getElementById('editEmail').value.trim(),
        phone_number: document.getElementById('editPhone').value.trim()
    };

    try {
        const response = await fetch(`${API_BASE_URL}/admin/student/${studentId}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${adminToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        const data = await response.json();
        if (data.success) {
            // Update cached student and refresh view
            _currentStudent = { ..._currentStudent, ...payload };
            displaySearchResult(_currentStudent);
            showSuccess('Student updated successfully!');
        } else {
            showError(data.message || 'Update failed');
        }
    } catch (e) {
        showError('Failed to update student. Please try again.');
    }
}

async function deleteStudent(studentId, registerNumber) {
    if (!confirm(`Are you sure you want to delete student ${registerNumber}? This will also remove all their attendance records.`)) return;

    try {
        const response = await fetch(`${API_BASE_URL}/admin/student/${studentId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${adminToken}` }
        });
        const data = await response.json();
        if (data.success) {
            document.getElementById('searchResult').style.display = 'none';
            _currentStudent = null;
            showSuccess('Student deleted successfully!');
            // Reload dashboard stats
            loadDashboard();
        } else {
            showError(data.message || 'Delete failed');
        }
    } catch (e) {
        showError('Failed to delete student. Please try again.');
    }
}

/* === EXPORT ALL EVENTS === */
async function exportAllAttendance() {
    showSuccess('Preparing export, please wait…');
    try {
        const response = await fetch(`${API_BASE_URL}/admin/export-all-attendance`, {
            headers: { 'Authorization': `Bearer ${adminToken}` }
        });
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `all_events_attendance_${Date.now()}.xlsx`;
            a.click();
            window.URL.revokeObjectURL(url);
            showSuccess('All events exported successfully!');
        } else {
            const data = await response.json();
            showError(data.message || 'Export failed');
        }
    } catch (e) {
        showError('Export failed. Please try again.');
    }
}

/* === COUNT-UP ANIMATION === */
function countUpAnimation(elementId, target, duration = 1200) {
    const el = document.getElementById(elementId);
    if (!el) return;
    const num = parseInt(target) || 0;
    if (num === 0) { el.textContent = 0; return; }
    const step = Math.max(1, Math.floor(num / (duration / 16)));
    let current = 0;
    const timer = setInterval(() => {
        current = Math.min(current + step, num);
        el.textContent = current;
        if (current >= num) clearInterval(timer);
    }, 16);
}

/* === CHART.JS CHARTS === */
let _attendanceChartInst = null;
let _departmentChartInst = null;

function initCharts(dashboard) {
    // Attendance bar chart
    const attCtx = document.getElementById('attendanceChart');
    if (attCtx && dashboard.event_registrations && dashboard.event_registrations.length) {
        if (_attendanceChartInst) _attendanceChartInst.destroy();
        _attendanceChartInst = new Chart(attCtx, {
            type: 'bar',
            data: {
                labels: dashboard.event_registrations.map(e => e.event_name),
                datasets: [{
                    label: 'Registered',
                    data: dashboard.event_registrations.map(e => e.total_registered || 0),
                    backgroundColor: 'rgba(99,102,241,0.75)',
                    borderRadius: 6
                }, {
                    label: 'Attended',
                    data: dashboard.event_registrations.map(e => e.total_attended || 0),
                    backgroundColor: 'rgba(16,185,129,0.75)',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { position: 'top' } },
                scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
            }
        });
    }

    // Department doughnut chart
    const deptCtx = document.getElementById('departmentChart');
    if (deptCtx && dashboard.department_stats && dashboard.department_stats.length) {
        if (_departmentChartInst) _departmentChartInst.destroy();
        const COLORS = [
            'rgba(99,102,241,0.85)',
            'rgba(16,185,129,0.85)',
            'rgba(245,158,11,0.85)',
            'rgba(239,68,68,0.85)',
            'rgba(6,182,212,0.85)',
            'rgba(168,85,247,0.85)'
        ];
        _departmentChartInst = new Chart(deptCtx, {
            type: 'doughnut',
            data: {
                labels: dashboard.department_stats.map(d => d.department),
                datasets: [{
                    data: dashboard.department_stats.map(d => d.count || 0),
                    backgroundColor: COLORS
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { position: 'bottom' } }
            }
        });
    }
}

// Load dashboard on page load
loadDashboard();
