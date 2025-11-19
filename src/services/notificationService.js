// Notification service for showing user feedback

/**
 * Shows a success notification
 * @param {string} message - The success message to display
 * @param {number} [duration=3000] - Duration in milliseconds to show the notification
 */
export const showSuccess = (message, duration = 3000) => {
  showNotification(message, 'success', duration);
};

/**
 * Shows an error notification
 * @param {string} message - The error message to display
 * @param {number} [duration=5000] - Duration in milliseconds to show the notification
 */
export const showError = (message, duration = 5000) => {
  showNotification(message, 'error', duration);
};

/**
 * Shows a warning notification
 * @param {string} message - The warning message to display
 * @param {number} [duration=4000] - Duration in milliseconds to show the notification
 */
export const showWarning = (message, duration = 4000) => {
  showNotification(message, 'warning', duration);
};

/**
 * Shows an info notification
 * @param {string} message - The info message to display
 * @param {number} [duration=3000] - Duration in milliseconds to show the notification
 */
export const showInfo = (message, duration = 3000) => {
  showNotification(message, 'info', duration);
};

/**
 * Clears all notifications
 */
export const clearNotifications = () => {
  const container = document.getElementById('notifications');
  if (container) {
    container.innerHTML = '';
  }
};

// Helper function to create and show a notification
const showNotification = (message, type = 'info', duration = 3000) => {
  // Ensure notifications container exists
  let container = document.getElementById('notifications');
  if (!container) {
    container = document.createElement('div');
    container.id = 'notifications';
    container.style.position = 'fixed';
    container.style.top = '20px';
    container.style.right = '20px';
    container.style.zIndex = '1000';
    document.body.appendChild(container);
  }

  // Create notification element
  const notification = document.createElement('div');
  notification.className = `notification ${type}`;
  notification.style.padding = '12px 24px';
  notification.style.margin = '8px 0';
  notification.style.borderRadius = '4px';
  notification.style.color = 'white';
  notification.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
  notification.style.animation = 'slideIn 0.3s ease-out';
  notification.style.transition = 'opacity 0.3s ease-out';
  
  // Set background color based on type
  const colors = {
    success: '#4caf50',
    error: '#f44336',
    warning: '#ff9800',
    info: '#2196f3'
  };
  
  notification.style.backgroundColor = colors[type] || colors.info;
  notification.textContent = message;

  // Add to container
  container.appendChild(notification);

  // Auto-remove after duration
  if (duration > 0) {
    setTimeout(() => {
      notification.style.opacity = '0';
      setTimeout(() => {
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification);
        }
      }, 300);
    }, duration);
  }

  // Add click to dismiss
  notification.onclick = () => {
    notification.style.opacity = '0';
    setTimeout(() => {
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification);
      }
    }, 300);
  };
};

// Add some basic styles if not already present
if (!document.getElementById('notification-styles')) {
  const style = document.createElement('style');
  style.id = 'notification-styles';
  style.textContent = `
    @keyframes slideIn {
      from { transform: translateX(100%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }
  `;
  document.head.appendChild(style);
}
