
const axios = require('axios');

async function testAPI() {
  try {
    // Test index route
    const indexResponse = await axios.get('http://localhost:5000/');
    console.log('Index Route:', indexResponse.data);
    
    // Test test_db route
    const testDBResponse = await axios.get('http://localhost:5000/test_db');
    console.log('Test DB Route:', testDBResponse.data);
    
    // Test nearest_stop route
    const nearestStopData = {
      latitude: 40.7128,
      longitude: -74.0060
    };
    const nearestStopResponse = await axios.post('http://localhost:5000/nearest_stop', nearestStopData);
    console.log('Nearest Stop:', nearestStopResponse.data);
    
    // Test plan_trip route
    const planTripData = {
      user_input: 'I need to go fast'
    };
    const planTripResponse = await axios.post('http://localhost:5000/plan_trip', planTripData);
    console.log('Plan Trip:', planTripResponse.data);
    
    // Test fare_info route
    const fareInfoData = {
      user_input: 'adult'
    };
    const fareInfoResponse = await axios.post('http://localhost:5000/fare_info', fareInfoData);
    console.log('Fare Info:', fareInfoResponse.data);
    
  } catch (error) {
    console.error('API Test Failed:', error);
  }
}

testAPI();
