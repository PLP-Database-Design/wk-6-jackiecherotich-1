const LS_USER = 'ccUser';
const USERS_KEY = 'ccUsers';

// Initialize users array in localStorage if it doesn't exist
if (!localStorage.getItem(USERS_KEY)) {
  localStorage.setItem(USERS_KEY, JSON.stringify([]));
}

// Register a new user
export function register(userData) {
  const users = JSON.parse(localStorage.getItem(USERS_KEY));
  
  // Check if user already exists
  const existingUser = users.find(u => u.email === userData.email);
  if (existingUser) {
    return { success: false, error: 'Email already registered' };
  }
  
  // Create new user
  const newUser = {
    id: Date.now().toString(),
    ...userData,
    createdAt: new Date().toISOString()
  };
  
  users.push(newUser);
  localStorage.setItem(USERS_KEY, JSON.stringify(users));
  
  // Auto-login the user after registration
  login(userData.email, userData.password);
  
  return { success: true, user: newUser };
}

// Login user
export function login(email, password) {
  const users = JSON.parse(localStorage.getItem(USERS_KEY));
  const user = users.find(u => u.email === email && u.password === password);
  
  if (!user) {
    return { success: false, error: 'Invalid credentials' };
  }
  
  // Store current user in localStorage
  localStorage.setItem(LS_USER, JSON.stringify(user));
  return { success: true, user };
}

// Logout user
export function logout() {
  localStorage.removeItem(LS_USER);
  return { success: true };
}

// Check if user is authenticated
export function isAuthenticated() {
  return !!localStorage.getItem(LS_USER);
}

// Get current user
export function getCurrentUser() {
  const saved = localStorage.getItem(LS_USER);
  return saved ? JSON.parse(saved) : null;
}

// Check if current user is admin
export function isAdmin() {
  const user = getCurrentUser();
  return user && user.role === 'admin';
}

// For testing purposes
export function _clearUsers() {
  localStorage.removeItem(USERS_KEY);
  localStorage.removeItem(LS_USER);
}