import { resetPassword, requestPasswordReset } from '../services/authService';

describe('Password Reset Functionality', () => {
  const testEmail = 'test@example.com';
  const newPassword = 'NewSecure@123';
  
  beforeEach(() => {
    // Clear any stored data before each test
    localStorage.clear();
    jest.clearAllMocks();
  });

  test('should generate and return a reset token for valid email', () => {
    // Mock the user in the system
    localStorage.setItem('users', JSON.stringify([{ email: testEmail }]));
    
    const result = requestPasswordReset(testEmail);
    
    expect(result.success).toBe(true);
    expect(result.resetToken).toBeDefined();
    expect(typeof result.resetToken).toBe('string');
    expect(result.resetToken.length).toBeGreaterThan(10); // Basic token length check
  });

  test('should return error for non-existent email', () => {
    const result = requestPasswordReset('nonexistent@example.com');
    
    expect(result.success).toBe(false);
    expect(result.error).toBe('Email not found');
  });

  test('should successfully reset password with valid token', () => {
    // First request a reset token
    localStorage.setItem('users', JSON.stringify([{ email: testEmail }]));
    const resetToken = requestPasswordReset(testEmail).resetToken;
    
    // Now try to reset the password
    const result = resetPassword(resetToken, newPassword);
    
    expect(result.success).toBe(true);
    expect(result.message).toBe('Password reset successful');
  });

  test('should reject invalid reset token', () => {
    const result = resetPassword('invalid-token-123', newPassword);
    
    expect(result.success).toBe(false);
    expect(result.error).toBe('Invalid or expired reset token');
  });

  test('should enforce password policy', () => {
    const weakPasswords = [
      'short',
      'noNumbersOrSymbols',
      '12345678',
      'lowercaseonly1',
      'UPPERCASEONLY1',
      'NoNumbers!',
      'noSpecial1'
    ];

    localStorage.setItem('users', JSON.stringify([{ email: testEmail }]));
    const resetToken = requestPasswordReset(testEmail).resetToken;
    
    weakPasswords.forEach(password => {
      const result = resetPassword(resetToken, password);
      expect(result.success).toBe(false);
      expect(result.error).toContain('Password must be at least 8 characters long');
    });
  });
});
