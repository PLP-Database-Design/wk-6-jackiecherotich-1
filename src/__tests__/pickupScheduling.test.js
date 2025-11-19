import { schedulePickup, getScheduledPickups, cancelPickup } from '../services/pickupService';

describe('Pickup Scheduling Service', () => {
  const testPickup = {
    userId: 'user123',
    address: '123 Test St, Test City',
    date: '2025-12-01',
    timeSlot: 'morning',
    wasteType: 'general',
    specialInstructions: 'Gate code: 1234'
  };

  beforeEach(() => {
    // Clear any stored data before each test
    localStorage.clear();
    jest.clearAllMocks();
  });

  test('should schedule a new pickup', () => {
    const result = schedulePickup(testPickup);
    
    expect(result.success).toBe(true);
    expect(result.pickup).toHaveProperty('id');
    expect(result.pickup.status).toBe('scheduled');
    expect(result.pickup.userId).toBe(testPickup.userId);
  });

  test('should retrieve scheduled pickups for a user', () => {
    // Schedule a pickup first
    schedulePickup(testPickup);
    
    const pickups = getScheduledPickups(testPickup.userId);
    
    expect(Array.isArray(pickups)).toBe(true);
    expect(pickups.length).toBe(1);
    expect(pickups[0].address).toBe(testPickup.address);
  });

  test('should cancel a scheduled pickup', () => {
    // Schedule a pickup first
    const scheduled = schedulePickup(testPickup);
    
    // Now cancel it
    const result = cancelPickup(scheduled.pickup.id, testPickup.userId);
    
    expect(result.success).toBe(true);
    expect(result.message).toBe('Pickup cancelled successfully');
    
    // Verify it's no longer in the scheduled pickups
    const pickups = getScheduledPickups(testPickup.userId);
    const cancelledPickup = pickups.find(p => p.id === scheduled.pickup.id);
    expect(cancelledPickup.status).toBe('cancelled');
  });

  test('should not allow scheduling in the past', () => {
    const pastDate = new Date();
    pastDate.setDate(pastDate.getDate() - 1);
    
    const invalidPickup = {
      ...testPickup,
      date: pastDate.toISOString().split('T')[0]
    };
    
    const result = schedulePickup(invalidPickup);
    
    expect(result.success).toBe(false);
    expect(result.error).toContain('Cannot schedule pickup in the past');
  });

  test('should enforce required fields', () => {
    const invalidPickup = { ...testPickup };
    delete invalidPickup.address;
    
    const result = schedulePickup(invalidPickup);
    
    expect(result.success).toBe(false);
    expect(result.error).toContain('Address is required');
  });
});
