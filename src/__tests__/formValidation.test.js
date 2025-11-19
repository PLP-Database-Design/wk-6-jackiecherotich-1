// Import form validation functions from your application
const { 
  validatePickupForm,
  validateFeedbackForm,
  validateRegistrationForm,
  validateLoginForm
} = require('../formValidation');

describe('Form Validation', () => {
  describe('Pickup Request Form', () => {
    test('should validate a valid pickup request', () => {
      const validData = {
        name: 'Test User',
        email: 'test@example.com',
        location: 'Nairobi',
        wasteType: 'General Waste',
        preferredDate: '2024-12-31',
        specialInstructions: 'Test instructions'
      };

      const result = validatePickupForm(validData);
      expect(result.isValid).toBe(true);
      expect(Object.keys(result.errors)).toHaveLength(0);
    });

    test('should reject missing required fields', () => {
      const invalidData = {
        name: '',
        email: 'invalid-email',
        location: '',
        wasteType: '',
        preferredDate: ''
      };

      const result = validatePickupForm(invalidData);
      expect(result.isValid).toBe(false);
      expect(result.errors).toHaveProperty('name');
      expect(result.errors).toHaveProperty('email');
      expect(result.errors).toHaveProperty('location');
      expect(result.errors).toHaveProperty('wasteType');
      expect(result.errors).toHaveProperty('preferredDate');
    });

    test('should validate email format', () => {
      const invalidEmailData = {
        name: 'Test User',
        email: 'invalid-email',
        location: 'Nairobi',
        wasteType: 'General Waste',
        preferredDate: '2024-12-31'
      };

      const result = validatePickupForm(invalidEmailData);
      expect(result.isValid).toBe(false);
      expect(result.errors.email).toContain('valid email');
    });
  });

  describe('Registration Form', () => {
    test('should validate a valid registration', () => {
      const validData = {
        name: 'Test User',
        email: 'test@example.com',
        password: 'StrongPass123!',
        confirmPassword: 'StrongPass123!',
        phone: '1234567890',
        address: '123 Test St, Nairobi'
      };

      const result = validateRegistrationForm(validData);
      expect(result.isValid).toBe(true);
    });

    test('should enforce strong password policy', () => {
      const weakPasswordData = {
        name: 'Test User',
        email: 'test@example.com',
        password: 'weak',
        confirmPassword: 'weak',
        phone: '1234567890'
      };

      const result = validateRegistrationForm(weakPasswordData);
      expect(result.isValid).toBe(false);
      expect(result.errors.password).toContain('stronger');
    });

    test('should match password and confirm password', () => {
      const mismatchData = {
        name: 'Test User',
        email: 'test@example.com',
        password: 'StrongPass123!',
        confirmPassword: 'DifferentPass123!',
        phone: '1234567890'
      };

      const result = validateRegistrationForm(mismatchData);
      expect(result.isValid).toBe(false);
      expect(result.errors.confirmPassword).toContain('match');
    });
  });

  describe('Login Form', () => {
    test('should validate a valid login', () => {
      const validData = {
        email: 'test@example.com',
        password: 'ValidPass123!'
      };

      const result = validateLoginForm(validData);
      expect(result.isValid).toBe(true);
    });

    test('should reject empty credentials', () => {
      const invalidData = {
        email: '',
        password: ''
      };

      const result = validateLoginForm(invalidData);
      expect(result.isValid).toBe(false);
      expect(result.errors.email).toBeDefined();
      expect(result.errors.password).toBeDefined();
    });
  });

  describe('Feedback Form', () => {
    test('should validate a valid feedback submission', () => {
      const validData = {
        name: 'Test User',
        email: 'test@example.com',
        subject: 'Test Subject',
        type: 'Suggestion',
        message: 'This is a test feedback message.'
      };

      const result = validateFeedbackForm(validData);
      expect(result.isValid).toBe(true);
    });

    test('should require a message', () => {
      const invalidData = {
        name: 'Test User',
        email: 'test@example.com',
        subject: 'Test Subject',
        type: 'Suggestion',
        message: ''
      };

      const result = validateFeedbackForm(invalidData);
      expect(result.isValid).toBe(false);
      expect(result.errors.message).toBeDefined();
    });
  });
});
