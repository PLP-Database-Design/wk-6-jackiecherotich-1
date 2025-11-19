// Mock API service for handling pickup requests
const API_BASE_URL = '/api';

// In-memory storage for demo purposes
let pickups = [];
let nextId = 1;

export const fetchPickups = async (userId) => {
  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 300));
  return pickups.filter(pickup => pickup.userId === userId);
};

export const schedulePickup = async (pickupData) => {
  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 300));
  
  const newPickup = {
    id: nextId++,
    ...pickupData,
    status: 'scheduled',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  };
  
  pickups.push(newPickup);
  return newPickup;
};

export const updatePickupStatus = async (pickupId, status, userId) => {
  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 300));
  
  const pickupIndex = pickups.findIndex(p => p.id === pickupId && p.userId === userId);
  if (pickupIndex === -1) {
    throw new Error('Pickup not found');
  }
  
  pickups[pickupIndex] = {
    ...pickups[pickupIndex],
    status,
    updatedAt: new Date().toISOString()
  };
  
  return pickups[pickupIndex];
};

export const getPickupById = async (pickupId, userId) => {
  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 200));
  
  const pickup = pickups.find(p => p.id === pickupId && p.userId === userId);
  if (!pickup) {
    throw new Error('Pickup not found');
  }
  return pickup;
};

// For testing purposes
export const _clearPickups = () => {
  pickups = [];
  nextId = 1;
};
