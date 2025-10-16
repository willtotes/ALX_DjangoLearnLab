// Main JavaScript file for Social Media API

// API Base URL
const API_BASE = '';

// Utility function to get CSRF token
function getCSRFToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Check authentication on page load
$(document).ready(function() {
    const token = localStorage.getItem('auth_token');
    const currentPath = window.location.pathname;
    
    // Public pages that don't require authentication
    const publicPages = ['/', '/login/', '/register/'];
    
    if (!token && !publicPages.includes(currentPath)) {
        window.location.href = '/login/';
        return;
    }
    
    if (token && publicPages.includes(currentPath) && currentPath !== '/') {
        window.location.href = '/feed/';
    }
    
    // Update notification badge on all pages
    if (token) {
        updateNotificationBadge();
    }
});

// Logout function
function logout() {
    const token = localStorage.getItem('auth_token');
    
    if (token) {
        $.ajax({
            url: '/api/auth/logout/',
            type: 'POST',
            headers: {
                'Authorization': `Token ${token}`
            },
            success: function() {
                localStorage.removeItem('auth_token');
                localStorage.removeItem('user');
                window.location.href = '/';
            },
            error: function() {
                // Still clear local storage even if API call fails
                localStorage.removeItem('auth_token');
                localStorage.removeItem('user');
                window.location.href = '/';
            }
        });
    } else {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user');
        window.location.href = '/';
    }
}

// Update notification badge
function updateNotificationBadge() {
    const token = localStorage.getItem('auth_token');
    
    if (!token) return;
    
    $.ajax({
        url: '/api/notifications/count/',
        type: 'GET',
        headers: {
            'Authorization': `Token ${token}`
        },
        success: function(response) {
            const $badge = $('#notification-badge');
            
            if (response.unread_count > 0) {
                $badge.text(response.unread_count).removeClass('d-none');
            } else {
                $badge.addClass('d-none');
            }
        },
        error: function() {
            // Silently fail - don't show error for notification count
        }
    });
}

// Format date relative to now
function formatRelativeTime(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);
    
    if (diffInSeconds < 60) {
        return 'just now';
    } else if (diffInSeconds < 3600) {
        const minutes = Math.floor(diffInSeconds / 60);
        return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    } else if (diffInSeconds < 86400) {
        const hours = Math.floor(diffInSeconds / 3600);
        return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    } else if (diffInSeconds < 604800) {
        const days = Math.floor(diffInSeconds / 86400);
        return `${days} day${days > 1 ? 's' : ''} ago`;
    } else {
        return date.toLocaleDateString();
    }
}

// Debounce function for search
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

// Show loading spinner
function showLoading($element) {
    $element.prop('disabled', true);
    $element.html('<div class="loading-spinner"></div>');
}

// Hide loading spinner
function hideLoading($element, originalText) {
    $element.prop('disabled', false);
    $element.text(originalText);
}

// Handle API errors
function handleApiError(xhr, $errorElement) {
    let message = 'An error occurred. Please try again.';
    
    if (xhr.responseJSON) {
        if (typeof xhr.responseJSON === 'string') {
            message = xhr.responseJSON;
        } else if (xhr.responseJSON.detail) {
            message = xhr.responseJSON.detail;
        } else if (xhr.responseJSON.non_field_errors) {
            message = xhr.responseJSON.non_field_errors.join(' ');
        } else {
            message = Object.values(xhr.responseJSON).flat().join(' ');
        }
    } else if (xhr.status === 0) {
        message = 'Network error. Please check your connection.';
    } else if (xhr.status === 401) {
        message = 'Please log in again.';
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user');
        setTimeout(() => window.location.href = '/login/', 2000);
    } else if (xhr.status === 403) {
        message = 'You do not have permission to perform this action.';
    } else if (xhr.status === 404) {
        message = 'The requested resource was not found.';
    } else if (xhr.status >= 500) {
        message = 'Server error. Please try again later.';
    }
    
    if ($errorElement) {
        $errorElement
            .removeClass('d-none alert-success')
            .addClass('alert-danger')
            .text(message);
    } else {
        alert(message);
    }
}

// Success message
function showSuccess(message, $element) {
    if ($element) {
        $element
            .removeClass('d-none alert-danger')
            .addClass('alert-success')
            .text(message);
    } else {
        alert(message);
    }
}

// Initialize tooltips
$(document).ready(function() {
    $('[data-bs-toggle="tooltip"]').tooltip();
});

// Auto-hide alerts after 5 seconds
$(document).ready(function() {
    setTimeout(function() {
        $('.alert').fadeOut(300, function() {
            $(this).remove();
        });
    }, 5000);
});