import { schedulePickup, fetchPickups, updatePickupStatus, getPickupById } from './apiService';

/**
 * Schedules a new waste pickup
 * @param {Object} pickupData - The pickup data including userId, address, date, timeSlot, wasteType, etc.
 * @returns {Promise<Object>} The created pickup object
 */
export const scheduleNewPickup = async (pickupData) => {
  try {
    // Validate required fields
    const requiredFields = ['userId', 'address', 'date', 'timeSlot', 'wasteType'];
    const missingFields = requiredFields.filter(field => !pickupData[field]);
    
    if (missingFields.length > 0) {
      throw new Error(`Missing required fields: ${missingFields.join(', ')}`);
    }

    // Validate date is in the future
    const pickupDate = new Date(pickupData.date);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    if (pickupDate < today) {
      throw new Error('Pickup date cannot be in the past');
    }

    // Call the API service
    return await schedulePickup(pickupData);
  } catch (error) {
    console.error('Error scheduling pickup:', error);
    throw error;
  }
};

/**
 * Gets all pickups for a user
 * @param {string} userId - The ID of the user
 * @returns {Promise<Array>} Array of pickup objects
 */
export const getUserPickups = async (userId) => {
  try {
    if (!userId) {
      throw new Error('User ID is required');
    }
    return await fetchPickups(userId);
  } catch (error) {
    console.error('Error fetching user pickups:', error);
    throw error;
  }
};

/**
 * Cancels a scheduled pickup
 * @param {string} pickupId - The ID of the pickup to cancel
 * @param {string} userId - The ID of the user making the request
 * @returns {Promise<Object>} The updated pickup object
 */
export const cancelScheduledPickup = async (pickupId, userId) => {
  try {
    if (!pickupId || !userId) {
      throw new Error('Pickup ID and User ID are required');
    }
    
    // First verify the pickup belongs to the user
    const pickup = await getPickupById(pickupId, userId);
    
    if (!pickup) {
      throw new Error('Pickup not found or access denied');
    }
    
    // Update the status to cancelled
    return await updatePickupStatus(pickupId, 'cancelled', userId);
  } catch (error) {
    console.error('Error cancelling pickup:', error);
    throw error;
  }
};

/**
 * Gets pickup details by ID
 * @param {string} pickupId - The ID of the pickup
 * @param {string} userId - The ID of the user making the request
 * @returns {Promise<Object>} The pickup details
 */
export const getPickupDetails = async (pickupId, userId) => {
  try {
    if (!pickupId || !userId) {
      throw new Error('Pickup ID and User ID are required');
    }
    return await getPickupById(pickupId, userId);
  } catch (error) {
    console.error('Error fetching pickup details:', error);
    throw error;
  }
};

/**
 * Checks if a time slot is available
 * @param {string} date - The date in YYYY-MM-DD format
 * @param {string} timeSlot - The time slot (e.g., 'morning', 'afternoon', 'evening')
 * @returns {Promise<boolean>} True if the time slot is available
 */
export const isTimeSlotAvailable = async (date, timeSlot) => {
  try {
    // In a real app, this would check against the database
    // For demo purposes, we'll assume all slots are available
    // except for a few hardcoded ones
    const unavailableSlots = {
      '2025-11-20': ['morning'],
      '2025-11-21': ['afternoon'],
    };
    
    const unavailable = unavailableSlots[date] || [];
    return !unavailable.includes(timeSlot);
  } catch (error) {
    console.error('Error checking time slot availability:', error);
    throw error;
  }
};

/**
 * Gets available time slots for a given date
 * @param {string} date - The date in YYYY-MM-DD format
 * @returns {Promise<Array>} Array of available time slots
 */
export const getAvailableTimeSlots = async (date) => {
  try {
    const allSlots = ['morning', 'afternoon', 'evening'];
    const availableSlots = [];
    
    for (const slot of allSlots) {
      const isAvailable = await isTimeSlotAvailable(date, slot);
      if (isAvailable) {
        availableSlots.push(slot);
      }
    }
    
    return availableSlots;
  } catch (error) {
    console.error('Error getting available time slots:', error);
    throw error;
  }
};
