// Frontend Configuration
const CONFIG = {
    // Backend API URL
    API_URL: 'http://localhost:8000/api',
    
    // Update this in production:
    // API_URL: 'https://your-backend.railway.app/api',
    
    // Feature flags
    FEATURES: {
        LEADERBOARD: true,
        SENIOR_MODE: true,
        ORG_DASHBOARD: true,
        INDIVIDUAL_MODE: true
    },
    
    // App settings
    APP_NAME: 'Aegis AI',
    VERSION: '1.0.0',
    
    // Difficulty levels
    DIFFICULTIES: ['easy', 'medium', 'hard'],
    
    // Departments
    DEPARTMENTS: [
        { key: 'accounting', name: 'Accounting', icon: '💰' },
        { key: 'hr', name: 'HR', icon: '🗂️' },
        { key: 'it', name: 'IT', icon: '🖥️' },
        { key: 'marketing', name: 'Marketing', icon: '📣' },
        { key: 'sales', name: 'Sales', icon: '📈' }
    ],
    
    // Sectors (individual mode)
    SECTORS: [
        { key: 'banking', name: 'Banking & Transfers', icon: '🏦' },
        { key: 'shopping', name: 'Online Shopping', icon: '🛍️' },
        { key: 'social', name: 'Social Media', icon: '📱' }
    ],
    
    // Points system
    POINTS: {
        CORRECT_PHISHING: 100,
        CORRECT_SAFE: 100,
        WRONG_CLASSIFICATION: 15,
        BONUS_ALL_FLAGS: 20
    },
    
    // Badges
    BADGES: {
        BRONZE: { threshold: 50, emoji: '🥉', name: 'Bronze' },
        SILVER: { threshold: 150, emoji: '🥈', name: 'Silver' },
        GOLD: { threshold: 300, emoji: '🥇', name: 'Gold' }
    }
};

// Export for modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}
