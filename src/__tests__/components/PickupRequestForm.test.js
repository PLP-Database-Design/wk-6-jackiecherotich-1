import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import PickupRequestForm from '../../components/PickupRequestForm';

// Mock any dependencies
jest.mock('../../services/dataService', () => ({
  addPickupRequest: jest.fn(() => ({
    success: true,
    request: {
      id: 'REQ123',
      status: 'Pending'
    }
  }))
}));

describe('PickupRequestForm Component', () => {
  const mockOnSuccess = jest.fn();
  
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
    
    // Render the component before each test
    render(<PickupRequestForm onSuccess={mockOnSuccess} />);
  });

  test('renders the form with all fields', () => {
    // Check that all form fields are rendered
    expect(screen.getByLabelText(/full name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/location/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/waste type/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/preferred date/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/special instructions/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /schedule pickup/i })).toBeInTheDocument();
  });

  test('validates form inputs before submission', async () => {
    // Try to submit empty form
    fireEvent.click(screen.getByRole('button', { name: /schedule pickup/i }));
    
    // Check for validation errors
    expect(await screen.findByText(/name is required/i)).toBeInTheDocument();
    expect(screen.getByText(/email is required/i)).toBeInTheDocument();
    expect(screen.getByText(/location is required/i)).toBeInTheDocument();
    expect(screen.getByText(/waste type is required/i)).toBeInTheDocument();
    expect(screen.getByText(/date is required/i)).toBeInTheDocument();
  });

  test('submits the form with valid data', async () => {
    // Fill in the form
    fireEvent.change(screen.getByLabelText(/full name/i), { 
      target: { value: 'Test User' } 
    });
    fireEvent.change(screen.getByLabelText(/email/i), { 
      target: { value: 'test@example.com' } 
    });
    fireEvent.change(screen.getByLabelText(/location/i), { 
      target: { value: 'Nairobi' } 
    });
    
    // Select waste type from dropdown
    fireEvent.change(screen.getByLabelText(/waste type/i), { 
      target: { value: 'General Waste' } 
    });
    
    // Set date (tomorrow)
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const dateString = tomorrow.toISOString().split('T')[0];
    fireEvent.change(screen.getByLabelText(/preferred date/i), { 
      target: { value: dateString } 
    });
    
    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /schedule pickup/i }));
    
    // Check that the form was submitted successfully
    expect(mockOnSuccess).toHaveBeenCalledTimes(1);
    expect(screen.getByText(/pickup scheduled successfully/i)).toBeInTheDocument();
  });

  test('shows error message when submission fails', async () => {
    // Mock a failed API call
    const errorMessage = 'Failed to schedule pickup';
    require('../../services/dataService').addPickupRequest.mockImplementationOnce(() => ({
      success: false,
      message: errorMessage
    }));
    
    // Fill in the form with minimal valid data
    fireEvent.change(screen.getByLabelText(/full name/i), { target: { value: 'Test User' } });
    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByLabelText(/location/i), { target: { value: 'Nairobi' } });
    fireEvent.change(screen.getByLabelText(/waste type/i), { target: { value: 'General Waste' } });
    
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const dateString = tomorrow.toISOString().split('T')[0];
    fireEvent.change(screen.getByLabelText(/preferred date/i), { target: { value: dateString } });
    
    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /schedule pickup/i }));
    
    // Check that the error message is displayed
    expect(await screen.findByText(errorMessage)).toBeInTheDocument();
  });
});
