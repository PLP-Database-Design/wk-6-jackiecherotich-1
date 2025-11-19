// Jest setup file
import '@testing-library/jest-dom';

// Mock localStorage
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: jest.fn((key) => store[key] || null),
    setItem: jest.fn((key, value) => {
      store[key] = String(value);
    }),
    removeItem: jest.fn((key) => {
      delete store[key];
    }),
    clear: jest.fn(() => {
      store = {};
    }),
  };
})();

// Mock the global localStorage
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

// Mock the global window.alert
global.alert = jest.fn();

// Mock the global console to prevent console errors in tests
global.console = {
  ...console,
  error: jest.fn(),
  warn: jest.fn(),
  log: jest.fn(),
};

// Add any other global mocks or configurations here
