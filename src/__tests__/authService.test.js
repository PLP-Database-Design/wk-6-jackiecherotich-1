const { login, register, logout, isAuthenticated, _clearUsers } = require('../services/authService');

describe('Authentication Service', () => {
  const testUser = {
    email: 'test@example.com',
    password: 'Test@123',
    name: 'Test User'
  };

  beforeEach(() => {
    // Clear users and reset state before each test
    _clearUsers();
    jest.clearAllMocks();
  });

  test('should register a new user', () => {
    const result = register(testUser);
    expect(result.success).toBe(true);
    expect(result.user).toHaveProperty('email', testUser.email);
  });

  test('should not register with existing email', () => {
    register(testUser);
    const result = register(testUser);
    expect(result.success).toBe(false);
    expect(result.error).toBe('Email already registered');
  });

  test('should login with valid credentials', () => {
    // First register the user
    register(testUser);
    // Then test login
    const result = login(testUser.email, testUser.password);
    expect(result.success).toBe(true);
    expect(isAuthenticated()).toBe(true);
  });

  test('should not login with invalid credentials', () => {
    register(testUser);
    const result = login(testUser.email, 'wrongpassword');
    expect(result.success).toBe(false);
    expect(isAuthenticated()).toBe(false);
  });

  test('should logout user', () => {
    // First register and login the user
    register(testUser);
    login(testUser.email, testUser.password);
    expect(isAuthenticated()).toBe(true);
    
    // Now test logout
    const result = logout();
    expect(result.success).toBe(true);
    expect(isAuthenticated()).toBe(false);
  });
});
