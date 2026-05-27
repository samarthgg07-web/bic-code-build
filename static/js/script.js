// ===========================
// Global JavaScript Functions
// ===========================

/**
 * Initialize app on document ready
 */
document.addEventListener('DOMContentLoaded', function() {
    initializeFormValidation();
    initializeTooltips();
    handlePageAnimations();
});

/**
 * Initialize Bootstrap form validation
 */
function initializeFormValidation() {
    // Get all forms that need validation
    const forms = document.querySelectorAll('form:not(.login-form)');

    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Real-time phone number validation
    const phoneInputs = document.querySelectorAll('input[name*="phone"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function() {
            // Remove non-numeric characters
            this.value = this.value.replace(/[^0-9]/g, '');
            // Limit to 10 digits
            this.value = this.value.substring(0, 10);
        });
    });

    // Convert USN to uppercase
    const usnInputs = document.querySelectorAll('input[name*="usn"]');
    usnInputs.forEach(input => {
        input.addEventListener('input', function() {
            this.value = this.value.toUpperCase();
        });
    });
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Handle page entrance animations
 */
function handlePageAnimations() {
    // Animate alert messages
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach((alert, index) => {
        alert.style.animation = `slideInDown 0.5s ease-out ${index * 0.1}s`;
    });

    // Animate cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate__animated', 'animate__fadeInUp');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all cards and detail cards
    const cards = document.querySelectorAll('.card, .detail-card, .stat-card');
    cards.forEach(card => {
        observer.observe(card);
    });
}

/**
 * Handle admin dashboard table row hover effects
 */
function initializeDashboardTable() {
    const tableRows = document.querySelectorAll('table tbody tr');

    tableRows.forEach((row, index) => {
        // Stagger animation
        row.style.animationDelay = `${index * 0.05}s`;

        // Add hover effects
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#f0f3f7';
        });

        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });
}

/**
 * Show loading spinner on form submission
 */
function showLoadingSpinner(buttonElement) {
    if (buttonElement) {
        buttonElement.disabled = true;
        const originalContent = buttonElement.innerHTML;
        buttonElement.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
        
        // Store original content for potential restoration
        buttonElement.dataset.originalContent = originalContent;
    }
}

/**
 * Hide loading spinner
 */
function hideLoadingSpinner(buttonElement) {
    if (buttonElement && buttonElement.dataset.originalContent) {
        buttonElement.innerHTML = buttonElement.dataset.originalContent;
        buttonElement.disabled = false;
    }
}

/**
 * Validate phone number format
 */
function validatePhoneNumber(phone) {
    const pattern = /^[6-9]\d{9}$/;
    return pattern.test(phone);
}

/**
 * Validate USN format
 */
function validateUSN(usn) {
    const pattern = /^[A-Z]{1,3}\d{2}[A-Z]{2}\d{3}$/;
    return pattern.test(usn.toUpperCase());
}

/**
 * Copy to clipboard utility
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showNotification('Copied to clipboard!', 'success');
    }, function(err) {
        showNotification('Failed to copy', 'error');
    });
}

/**
 * Show temporary notification
 */
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(alertDiv);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

/**
 * Format date to readable format
 */
function formatDate(dateString) {
    const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit' 
    };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

/**
 * Export table to CSV
 */
function exportTableToCSV(filename = 'export.csv') {
    const table = document.querySelector('table');
    if (!table) return;

    let csv = [];
    const rows = table.querySelectorAll('tr');

    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        let csvRow = [];
        cols.forEach(col => {
            csvRow.push('"' + col.innerText.replace(/"/g, '""') + '"');
        });
        csv.push(csvRow.join(','));
    });

    downloadCSV(csv.join('\n'), filename);
}

/**
 * Download CSV file
 */
function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], { type: 'text/csv' });
    const downloadLink = document.createElement('a');
    downloadLink.href = URL.createObjectURL(csvFile);
    downloadLink.download = filename;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

/**
 * Debounce function for search
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Print page functionality
 */
function printPage() {
    window.print();
}

/**
 * Smooth scroll to element
 */
function smoothScroll(elementSelector) {
    const element = document.querySelector(elementSelector);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Check if user is online
 */
function isOnline() {
    return navigator.onLine;
}

/**
 * Handle offline/online status
 */
window.addEventListener('online', function() {
    showNotification('You are back online!', 'success');
});

window.addEventListener('offline', function() {
    showNotification('You are offline. Some features may not work.', 'warning');
});

// ===========================
// Initialization for specific pages
// ===========================

// Initialize dashboard if on dashboard page
if (document.querySelector('.admin-dashboard-container')) {
    document.addEventListener('DOMContentLoaded', initializeDashboardTable);
}

// Add keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + K for search focus
    if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        const searchInput = document.getElementById('search');
        if (searchInput) {
            searchInput.focus();
        }
    }
});
