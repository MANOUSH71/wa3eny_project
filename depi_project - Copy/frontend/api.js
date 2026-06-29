// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';

// API Helper Functions
const api = {
    async post(endpoint, data) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error(`API Error: ${response.statusText}`);
        return response.json();
    },
    
    async get(endpoint) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`);
        if (!response.ok) throw new Error(`API Error: ${response.statusText}`);
        return response.json();
    },

    // Scenarios
    generateScenario: (department, sector, difficulty = 'medium') => 
        api.post('/scenarios/generate', { department, sector, difficulty }),
    
    classifyScenario: (scenarioId, userClassification, selectedFlags) =>
        api.post('/scenarios/classify', { scenario_id: scenarioId, user_classification: userClassification, selected_flags: selectedFlags }),

    // Organizations
    getOrgStats: () => api.get('/organizations/stats'),
    
    updateDepartment: (departmentKey, score, correct) =>
        api.post('/organizations/departments/update', { department_key: departmentKey, score, correct }),

    // Users
    createUser: (name, email) => api.post('/users/', { name, email, points: 0 }),
    
    getUser: (userId) => api.get(`/users/${userId}`),

    // Leaderboard
    getLeaderboard: (limit = 10) => api.get(`/leaderboard/?limit=${limit}`)
};

// Example Usage (commented out):
/*
// Generate scenario
const scenario = await api.generateScenario('accounting', null, 'medium');

// Classify scenario
const result = await api.classifyScenario(
    scenario.id, 
    true,  // user thinks it's phishing
    ['Urgent request', 'Strange link']
);

// Get leaderboard
const leaderboard = await api.getLeaderboard(10);
*/
