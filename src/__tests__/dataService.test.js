// Mock localStorage
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: jest.fn((key) => store[key] || null),
    setItem: jest.fn((key, value) => {
      store[key] = value.toString();
    }),
    removeItem: jest.fn((key) => {
      delete store[key];
    }),
    clear: jest.fn(() => {
      store = {};
    }),
  };
})();

global.localStorage = localStorageMock;

// Import the data service
const dataService = require('../dataService');

describe('Data Service', () => {
  beforeEach(() => {
    // Clear all mocks and localStorage before each test
    jest.clearAllMocks();
    localStorage.clear();
  });

  describe('Pickup Requests', () => {
    test('should add a new pickup request', () => {
      const requestData = {
        name: 'Test User',
        email: 'test@example.com',
        location: 'Nairobi',
        wasteType: 'General Waste',
        preferredDate: '2024-12-31',
        specialInstructions: 'Test instructions'
      };

      const result = dataService.addPickupRequest(requestData);
      
      expect(result.success).toBe(true);
      expect(result.request).toHaveProperty('id');
      expect(result.request.status).toBe('Pending');
      expect(localStorage.setItem).toHaveBeenCalled();
    });

    test('should get all pickup requests', () => {
      // First add a request
      const requestData = {
        name: 'Test User',
        email: 'test@example.com',
        location: 'Nairobi',
        wasteType: 'Recyclable',
        preferredDate: '2024-12-31'
      };
      dataService.addPickupRequest(requestData);

      const requests = dataService.getAllPickupRequests();
      
      expect(Array.isArray(requests)).toBe(true);
      expect(requests.length).toBeGreaterThan(0);
      expect(requests[0].wasteType).toBe('Recyclable');
    });

    test('should filter requests by status', () => {
      // Add multiple requests with different statuses
      dataService.addPickupRequest({
        name: 'User 1',
        email: 'user1@example.com',
        location: 'Nairobi',
        wasteType: 'General Waste',
        preferredDate: '2024-12-31',
        status: 'Pending'
      });
      
      dataService.addPickupRequest({
        name: 'User 2',
        email: 'user2@example.com',
        location: 'Mombasa',
        wasteType: 'Hazardous',
        preferredDate: '2024-12-30',
        status: 'Completed'
      });

      const pendingRequests = dataService.filterRequestsByStatus('Pending');
      expect(pendingRequests.every(req => req.status === 'Pending')).toBe(true);
      
      const completedRequests = dataService.filterRequestsByStatus('Completed');
      expect(completedRequests.every(req => req.status === 'Completed')).toBe(true);
    });
  });

  describe('User Management', () => {
    test('should register a new user', () => {
      const userData = {
        name: 'Test User',
        email: 'test@example.com',
        password: 'Test@1234',
        phone: '1234567890',
        address: '123 Test St, Nairobi'
      };

      const result = dataService.addUser(userData);
      
      expect(result.success).toBe(true);
      expect(result.user).toHaveProperty('id');
      expect(result.user.email).toBe(userData.email);
      expect(localStorage.setItem).toHaveBeenCalled();
    });

    test('should not allow duplicate email registration', () => {
      const userData = {
        name: 'Test User',
        email: 'duplicate@example.com',
        password: 'Test@1234',
        phone: '1234567890'
      };

      // First registration should succeed
      const firstAttempt = dataService.addUser(userData);
      expect(firstAttempt.success).toBe(true);

      // Second registration with same email should fail
      const secondAttempt = dataService.addUser(userData);
      expect(secondAttempt.success).toBe(false);
      expect(secondAttempt.message).toContain('already exists');
    });

    test('should authenticate user with correct credentials', () => {
      // First register a user
      const userData = {
        name: 'Auth User',
        email: 'auth@example.com',
        password: 'Auth@1234',
        phone: '1234567890'
      };
      dataService.addUser(userData);

      // Test login with correct credentials
      const loginResult = dataService.login(userData.email, userData.password);
      expect(loginResult.success).toBe(true);
      expect(loginResult.user).toBeDefined();
      expect(loginResult.user.email).toBe(userData.email);
    });

    test('should reject invalid login credentials', () => {
      // Test with non-existent user
      const invalidLogin = dataService.login('nonexistent@example.com', 'wrongpass');
      expect(invalidLogin.success).toBe(false);
      expect(invalidLogin.message).toContain('Invalid');
    });
  });

  describe('Feedback System', () => {
    test('should add new feedback', () => {
      const feedbackData = {
        name: 'Feedback User',
        email: 'feedback@example.com',
        subject: 'Test Feedback',
        type: 'Suggestion',
        message: 'This is a test feedback message.'
      };

      const result = dataService.addFeedback(feedbackData);
      
      expect(result.success).toBe(true);
      expect(result.feedback).toHaveProperty('id');
      expect(result.feedback.subject).toBe(feedbackData.subject);
      
      // Verify feedback was saved
      const allFeedback = dataService.getAllFeedback();
      expect(allFeedback.some(fb => fb.id === result.feedback.id)).toBe(true);
    });
  });
});
