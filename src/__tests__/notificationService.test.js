import { showSuccess, showError, clearNotifications } from '../services/notificationService';

describe('Notification Service', () => {
  beforeEach(() => {
    // Clear any existing notifications before each test
    clearNotifications();
    document.body.innerHTML = '<div id="notifications"></div>';
  });

  test('should show success notification', () => {
    const message = 'Operation completed successfully';
    showSuccess(message);
    
    const notification = document.querySelector('.notification.success');
    expect(notification).not.toBeNull();
    expect(notification.textContent).toContain(message);
  });

  test('should show error notification', () => {
    const message = 'An error occurred';
    showError(message);
    
    const notification = document.querySelector('.notification.error');
    expect(notification).not.toBeNull();
    expect(notification.textContent).toContain(message);
  });

  test('should clear all notifications', () => {
    showSuccess('Test message');
    showError('Error message');
    
    clearNotifications();
    
    const notifications = document.querySelectorAll('.notification');
    expect(notifications.length).toBe(0);
  });

  test('should auto-remove notification after timeout', (done) => {
    jest.useFakeTimers();
    
    const message = 'Temporary message';
    showSuccess(message, 1000);
    
    // Fast-forward time
    jest.advanceTimersByTime(1000);
    
    const notification = document.querySelector('.notification');
    expect(notification).toBeNull();
    
    jest.useRealTimers();
    done();
  });
});
