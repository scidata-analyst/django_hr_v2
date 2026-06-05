/**
 * @file constants.js
 * @description Centralized API endpoint constants.
 *              All routes are prefixed under `/talent-growth/` matching Django URL routes.
 */

/**
 * @constant {Object} API_ENDPOINTS
 * @description API endpoint URLs for talent growth module.
 *              Static properties return a string; dynamic ones accept an `id` and return a string.
 */
const API_ENDPOINTS = {
    TRAINING: {
        COURSES: {
            INDEX: '/talent-growth/training/api/course/',
            STORE: '/talent-growth/training/api/course/',
            SHOW: (id) => `/talent-growth/training/api/course/${id}/`,
            UPDATE: (id) => `/talent-growth/training/api/course/${id}/`,
            DESTROY: (id) => `/talent-growth/training/api/course/${id}/`,
        },
        ENROLLMENTS: {
            INDEX: '/talent-growth/training/api/enrollment/',
            STORE: '/talent-growth/training/api/enrollment/',
            COMPLETE: (id) => `/talent-growth/training/api/enrollment/${id}/complete/`,
            BULK: '/talent-growth/training/api/enrollment/bulk/',
        },
    },

    TALENT: {
        PROFILES: {
            INDEX: '/talent-growth/talent/api/profile/',
        },
        SUCCESSION: {
            INDEX: '/talent-growth/talent/api/succession/',
        },
    },

    PERFORMANCE: {
        REVIEWS: {
            INDEX: '/talent-growth/performance/api/review/',
            COMPLETE: (id) => `/talent-growth/performance/api/review/${id}/complete/`,
        },
        GOALS: {
            INDEX: '/talent-growth/performance/api/goal/',
            PROGRESS: (id) => `/talent-growth/performance/api/goal/${id}/progress/`,
        },
    },

    ENGAGEMENT: {
        SURVEYS: {
            INDEX: '/talent-growth/engagement/api/survey/',
        },
        RECOGNITION: {
            INDEX: '/talent-growth/engagement/api/recognition/',
            EMPLOYEE_POINTS: (employeeId) => `/talent-growth/engagement/api/recognition/${employeeId}/points/`,
        },
    },
};

/**
 * @constant {Object} API_CONFIG
 * @description Global API configuration applied to all requests.
 * @property {string} BASE_URL    - Base URL prepended to all endpoints (empty = same origin).
 * @property {number} TIMEOUT     - Request timeout in milliseconds.
 * @property {Object} HEADERS     - Default HTTP headers sent with every request.
 */
const API_CONFIG = {
    BASE_URL: '',
    TIMEOUT: 10000,
    HEADERS: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    },
};