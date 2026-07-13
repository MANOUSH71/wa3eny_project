// ========================================
// Wa3eny Frontend API Configuration
// ========================================

const API_BASE_URL = 'http://127.0.0.1:8000/api';


// ========================================
// Local Storage Auth Helpers
// ========================================

function getAuthToken() {
    return localStorage.getItem('token');
}

function getCurrentUser() {
    const userString = localStorage.getItem('user');

    if (!userString) {
        return null;
    }

    try {
        return JSON.parse(userString);
    } catch (error) {
        console.error('Failed to parse stored user:', error);
        localStorage.removeItem('user');
        return null;
    }
}

function loginUser(tokenResponse) {
    if (!tokenResponse?.access_token) {
        throw new Error('Authentication token was not returned by the server.');
    }

    localStorage.setItem('token', tokenResponse.access_token);

    if (tokenResponse.user) {
        localStorage.setItem(
            'user',
            JSON.stringify(tokenResponse.user)
        );
    }
}

function logoutUser() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
}

function isLoggedIn() {
    return Boolean(getAuthToken());
}


// ========================================
// Error Handling
// ========================================

async function readErrorResponse(response) {
    try {
        const data = await response.json();

        if (typeof data.detail === 'string') {
            return data.detail;
        }

        if (Array.isArray(data.detail)) {
            return data.detail
                .map(item => item.msg || JSON.stringify(item))
                .join(', ');
        }

        return data.message || `Request failed with status ${response.status}`;
    } catch (error) {
        return `Request failed with status ${response.status}: ${response.statusText}`;
    }
}


// ========================================
// General API Helper
// ========================================

async function apiRequest(
    endpoint,
    {
        method = 'GET',
        body = null,
        isFormData = false,
        requiresAuth = true
    } = {}
) {
    const headers = {};

    if (!isFormData && body !== null) {
        headers['Content-Type'] = 'application/json';
    }

    if (requiresAuth) {
        const token = getAuthToken();

        if (token) {
            headers.Authorization = `Bearer ${token}`;
        }
    }

    const options = {
        method,
        headers
    };

    if (body !== null) {
        options.body = isFormData
            ? body
            : JSON.stringify(body);
    }

    let response;

    try {
        response = await fetch(
            `${API_BASE_URL}${endpoint}`,
            options
        );
    } catch (error) {
        console.error('Network error:', error);

        throw new Error(
            'Unable to connect to the backend. Make sure python run.py is running.'
        );
    }

    if (!response.ok) {
        const message = await readErrorResponse(response);

        if (response.status === 401) {
            // Do not automatically clear token during login.
            if (endpoint !== '/auth/login') {
                logoutUser();
            }
        }

        throw new Error(message);
    }

    if (response.status === 204) {
        return null;
    }

    return response.json();
}


// ========================================
// API Methods
// ========================================

const api = {

    // ------------------------------------
    // Generic methods
    // ------------------------------------

    get(endpoint, requiresAuth = true) {
        return apiRequest(endpoint, {
            method: 'GET',
            requiresAuth
        });
    },

    post(endpoint, data, requiresAuth = true) {
        return apiRequest(endpoint, {
            method: 'POST',
            body: data,
            requiresAuth
        });
    },


    // ------------------------------------
    // Authentication
    // ------------------------------------

    register(
        name,
        email,
        password,
        role,
        organizationName = null
    ) {
        const payload = {
            name,
            email,
            password,
            role,
            organization_name: organizationName
        };

        return apiRequest('/auth/register', {
            method: 'POST',
            body: payload,
            requiresAuth: false
        });
    },

    async login(email, password) {
        const formData = new FormData();

        // FastAPI OAuth2PasswordRequestForm expects "username"
        formData.append('username', email);
        formData.append('password', password);

        return apiRequest('/auth/login', {
            method: 'POST',
            body: formData,
            isFormData: true,
            requiresAuth: false
        });
    },

    getMe() {
        return api.get('/auth/me');
    },

    joinOrganization(
        name,
        email,
        password,
        organizationCode,
        department
    ) {
        return apiRequest('/auth/join-organization', {
            method: 'POST',
            body: {
                name,
                email,
                password,
                organization_code: organizationCode,
                department
            },
            requiresAuth: false
        });
    },


    // ------------------------------------
    // Organization
    // ------------------------------------

    getMyOrganization() {
        return api.get('/organizations/me');
    },

    getOrganizationByCode(organizationCode) {
        return api.get(
            `/organizations/code/${encodeURIComponent(organizationCode)}`,
            false
        );
    },

    getOrgStats() {
        return api.get('/organizations/stats');
    },

    updateDepartment(departmentKey, score, correct) {
        return api.post('/organizations/departments/update', {
            department_key: departmentKey,
            score,
            correct
        });
    },


    // ------------------------------------
    // Employees
    // ------------------------------------

    getEmployees() {
        return api.get('/employees');
    },


    // ------------------------------------
    // Scenarios
    // ------------------------------------

    generateScenario(
        department,
        sector = null,
        difficulty = 'medium'
    ) {
        return api.post('/scenarios/generate', {
            department,
            sector,
            difficulty
        });
    },

    classifyScenario(
        scenarioId,
        userClassification,
        selectedFlags
    ) {
        return api.post('/scenarios/classify', {
            scenario_id: scenarioId,
            user_classification: userClassification,
            selected_flags: selectedFlags
        });
    },


    // ------------------------------------
    // Users
    // ------------------------------------

    createUser(name, email) {
        return api.post('/users/', {
            name,
            email,
            points: 0
        });
    },

    getUser(userId) {
        return api.get(
            `/users/${encodeURIComponent(userId)}`
        );
    },


    // ------------------------------------
    // Leaderboard
    // ------------------------------------

    getLeaderboard(limit = 10) {
        return api.get(
            `/leaderboard/?limit=${encodeURIComponent(limit)}`,
            false
        );
    }
};