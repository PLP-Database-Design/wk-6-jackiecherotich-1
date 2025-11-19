const { 
  fetchPickups, 
  schedulePickup, 
  updatePickupStatus, 
  _clearPickups: clearPickups // Renamed to avoid lint warning
} = require('../services/apiService');
const { setupServer } = require('msw/node');
const { rest } = require('msw');

const server = setupServer(
  rest.get('/api/pickups', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json([
        { id: 1, status: 'scheduled', date: '2023-11-20' },
        { id: 2, status: 'completed', date: '2023-11-19' }
      ])
    );
  }),
  
  rest.post('/api/pickups', (req, res, ctx) => {
    return res(
      ctx.status(201),
      ctx.json({ 
        id: 3, 
        ...req.body,
        status: 'scheduled',
        createdAt: new Date().toISOString()
      })
    );
  }),
  
  rest.patch('/api/pickups/:id', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        ...req.body,
        id: req.params.id,
        updatedAt: new Date().toISOString()
      })
    );
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('API Service', () => {
  test('should fetch pickups', async () => {
    const pickups = await fetchPickups();
    expect(pickups).toHaveLength(2);
    expect(pickups[0]).toHaveProperty('id');
    expect(pickups[0]).toHaveProperty('status');
  });

  test('should schedule a new pickup', async () => {
    const pickupData = {
      date: '2023-11-25',
      timeSlot: 'morning',
      address: '123 Test St',
      wasteType: 'general',
      notes: 'Test pickup'
    };
    
    const result = await schedulePickup(pickupData);
    expect(result).toHaveProperty('id');
    expect(result.status).toBe('scheduled');
    expect(result).toMatchObject(pickupData);
  });

  test('should update pickup status', async () => {
    const updateData = { status: 'in-progress' };
    const result = await updatePickupStatus(1, updateData);
    expect(result).toMatchObject(updateData);
    expect(result).toHaveProperty('id', '1');
  });

  test('should handle API errors', async () => {
    server.use(
      rest.get('/api/pickups', (req, res, ctx) => {
        return res(
          ctx.status(500),
          ctx.json({ message: 'Internal Server Error' })
        );
      })
    );

    await expect(fetchPickups()).rejects.toThrow('Request failed with status code 500');
  });
});
