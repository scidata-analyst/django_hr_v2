/**
 * @file constants.js
 * @description Centralized API endpoint constants.
 *              All routes are prefixed under `/operation/` matching Django URL routes.
 */

/**
 * @constant {Object} API_ENDPOINTS
 * @description API endpoint URLs for operation module.
 *              Static properties return a string; dynamic ones accept an `id` and return a string.
 */
const API_ENDPOINTS = {
    BENEFITS: {
        PLANS: {
            INDEX: '/operation/api/benefit-plan/',
            STORE: '/operation/api/benefit-plan/',
            SHOW: (id) => `/operation/api/benefit-plan/${id}/`,
            UPDATE: (id) => `/operation/api/benefit-plan/${id}/`,
            DESTROY: (id) => `/operation/api/benefit-plan/${id}/`,
        },
        ENROLLMENTS: {
            INDEX: '/operation/api/benefit-enrollment/',
            STORE: '/operation/api/benefit-enrollment/',
        },
    },

    SAFETY: {
        INCIDENTS: {
            INDEX: '/operation/api/safety-incident/',
            STORE: '/operation/api/safety-incident/',
            RESOLVE: (id) => `/operation/api/safety-incident/${id}/resolve/`,
        },
    },

    POLICIES: {
        INDEX: '/operation/api/policy/',
        STORE: '/operation/api/policy/',
        SHOW: (id) => `/operation/api/policy/${id}/`,
        UPDATE: (id) => `/operation/api/policy/${id}/`,
        DESTROY: (id) => `/operation/api/policy/${id}/`,
        ACKNOWLEDGE: (id) => `/operation/api/policy/${id}/acknowledge/`,
    },

    COMPLIANCE: {
        INDEX: '/operation/api/compliance/',
        COMPLETE: (id) => `/operation/api/compliance/${id}/complete/`,
    },

    REPORTS: {
        HEADCOUNT: '/operation/api/report/headcount/',
        ATTENDANCE: '/operation/api/report/attendance/',
        TURNOVER: '/operation/api/report/turnover/',
    },

    INTEGRATIONS: {
        INDEX: '/operation/api/integration/',
        TOGGLE: (id) => `/operation/api/integration/${id}/toggle/`,
    },

    OFFICES: {
        INDEX: '/operation/global/api/office/',
        STORE: '/operation/global/api/office/',
        SHOW: (id) => `/operation/global/api/office/${id}/`,
        UPDATE: (id) => `/operation/global/api/office/${id}/`,
        DESTROY: (id) => `/operation/global/api/office/${id}/`,
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