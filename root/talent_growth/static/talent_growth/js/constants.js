/**
 * @file constants.js
 * @description Centralized API endpoint constants.
 *              All routes are prefixed under `/core-module/` matching Django URL routes.
 */

/**
 * @constant {Object} API_ENDPOINTS
 * @description API endpoint URLs for HR core modules.
 *              Static properties return a string; dynamic ones accept an `id` and return a string.
 */
const API_ENDPOINTS = {
    /**
     * @namespace ATTENDANCE
     * @description Attendance management - shifts, attendance, and leave tracking.
     * @see core_module/routes/attendance/attendance.py
     * @routePrefix core-module.attendance
     */
    ATTENDANCE: {
        /** @routePrefix core-module.attendance.shifts */
        SHIFTS: {
            INDEX: '/core-module/attendance/api/shift/',
            STORE: '/core-module/attendance/api/shift/',
            SHOW: (id) => `/core-module/attendance/api/shift/${id}/`,
            UPDATE: (id) => `/core-module/attendance/api/shift/${id}/`,
            DESTROY: (id) => `/core-module/attendance/api/shift/${id}/`,
        },
        /** @routePrefix core-module.attendance.attendance */
        RECORDS: {
            INDEX: '/core-module/attendance/api/attendance/',
            STORE: '/core-module/attendance/api/attendance/',
            SHOW: (id) => `/core-module/attendance/api/attendance/${id}/`,
            UPDATE: (id) => `/core-module/attendance/api/attendance/${id}/`,
            DESTROY: (id) => `/core-module/attendance/api/attendance/${id}/`,
        },
        /** @routePrefix core-module.attendance.stats */
        STATS: {
            INDEX: '/core-module/attendance/api/attendance/stats/',
            EMPLOYEE_STATS: (employeeId) => `/core-module/attendance/api/attendance/${employeeId}/stats/`,
        },
        /** @routePrefix core-module.attendance.leaves */
        LEAVES: {
            INDEX: '/core-module/attendance/api/leave/',
            STORE: '/core-module/attendance/api/leave/',
            SHOW: (id) => `/core-module/attendance/api/leave/${id}/`,
            UPDATE: (id) => `/core-module/attendance/api/leave/${id}/`,
            DESTROY: (id) => `/core-module/attendance/api/leave/${id}/`,
            APPROVE: (id) => `/core-module/attendance/api/leave/${id}/approve/`,
            DENY: (id) => `/core-module/attendance/api/leave/${id}/deny/`,
        },
    },

    /**
     * @namespace RECRUITMENT
     * @description Recruitment management - job postings, candidates, and interviews.
     * @see core_module/routes/recruitment/recruitment.py
     * @routePrefix core-module.recruitment
     */
    RECRUITMENT: {
        JOBS: {
            INDEX: '/core-module/recruitment/api/job/',
            STORE: '/core-module/recruitment/api/job/',
            SHOW: (id) => `/core-module/recruitment/api/job/${id}/`,
            UPDATE: (id) => `/core-module/recruitment/api/job/${id}/`,
            DESTROY: (id) => `/core-module/recruitment/api/job/${id}/`,
        },
        CANDIDATES: {
            INDEX: '/core-module/recruitment/api/candidate/',
            STORE: '/core-module/recruitment/api/candidate/',
            SHOW: (id) => `/core-module/recruitment/api/candidate/${id}/`,
            UPDATE: (id) => `/core-module/recruitment/api/candidate/${id}/`,
            DESTROY: (id) => `/core-module/recruitment/api/candidate/${id}/`,
            ADVANCE: (id) => `/core-module/recruitment/api/candidate/${id}/advance/`,
            REJECT: (id) => `/core-module/recruitment/api/candidate/${id}/reject/`,
        },
        PIPELINE: {
            INDEX: '/core-module/recruitment/api/candidate/pipeline/',
        },
        INTERVIEWS: {
            INDEX: '/core-module/recruitment/api/interview/',
            RESULT: (id) => `/core-module/recruitment/api/interview/${id}/result/`,
        },
    },

    /**
     * @namespace PAYROLL
     * @description Payroll management - salary structures, payslips, and bonuses.
     * @see core_module/routes/payroll/payroll.py
     * @routePrefix core-module.payroll
     */
    PAYROLL: {
        SALARY_STRUCTURES: {
            INDEX: '/core-module/payroll/api/structure/',
            STORE: '/core-module/payroll/api/structure/',
            SHOW: (id) => `/core-module/payroll/api/structure/${id}/`,
            UPDATE: (id) => `/core-module/payroll/api/structure/${id}/`,
            DESTROY: (id) => `/core-module/payroll/api/structure/${id}/`,
        },
        PAYSLIPS: {
            INDEX: '/core-module/payroll/api/payslip/',
            STORE: '/core-module/payroll/api/payslip/',
            SHOW: (id) => `/core-module/payroll/api/payslip/${id}/`,
            BULK_GENERATE: '/core-module/payroll/api/payslip/bulk-generate/',
        },
        LOANS: {
            INDEX: '/core-module/payroll/api/loan/',
            STORE: '/core-module/payroll/api/loan/',
            SHOW: (id) => `/core-module/payroll/api/loan/${id}/`,
            APPROVE: (id) => `/core-module/payroll/api/loan/${id}/approve/`,
        },
        BONUSES: {
            INDEX: '/core-module/payroll/api/bonus/',
            STORE: '/core-module/payroll/api/bonus/',
            SHOW: (id) => `/core-module/payroll/api/bonus/${id}/`,
        },
    },

    /**
     * @namespace ONBOARDING
     * @description Onboarding management - tasks and offboarding.
     * @see core_module/routes/onboarding/onboarding.py
     * @routePrefix core-module.onboarding
     */
    ONBOARDING: {
        TASKS: {
            INDEX: '/core-module/onboarding/api/task/',
            STORE: '/core-module/onboarding/api/task/',
            SHOW: (id) => `/core-module/onboarding/api/task/${id}/`,
            UPDATE: (id) => `/core-module/onboarding/api/task/${id}/`,
            DESTROY: (id) => `/core-module/onboarding/api/task/${id}/`,
        },
        OFFBOARDING: {
            INDEX: '/core-module/onboarding/api/offboarding/',
        },
        EXIT_INTERVIEWS: {
            INDEX: '/core-module/onboarding/api/exit-interview/',
        },
    },

    /**
     * @namespace ESS
     * @description Employee self-service - expenses and announcements.
     * @see core_module/routes/ess/ess.py
     * @routePrefix core-module.ess
     */
    ESS: {
        EXPENSES: {
            INDEX: '/core-module/ess/api/expense/',
            STORE: '/core-module/ess/api/expense/',
            SHOW: (id) => `/core-module/ess/api/expense/${id}/`,
            APPROVE: (id) => `/core-module/ess/api/expense/${id}/approve/`,
            REJECT: (id) => `/core-module/ess/api/expense/${id}/reject/`,
        },
        ANNOUNCEMENTS: {
            INDEX: '/core-module/ess/api/announcement/',
            STORE: '/core-module/ess/api/announcement/',
            SHOW: (id) => `/core-module/ess/api/announcement/${id}/`,
        },
    },

    /**
     * @namespace EMPLOYEE
     * @description Employee management - employees, departments, locations, and designations.
     * @see core_module/routes/employee/employee.py
     * @routePrefix core-module.employee
     */
    EMPLOYEE: {
        DEPARTMENTS: {
            INDEX: '/core-module/employee/api/department/',
            STORE: '/core-module/employee/api/department/',
            SHOW: (id) => `/core-module/employee/api/department/${id}/`,
            UPDATE: (id) => `/core-module/employee/api/department/${id}/`,
            DESTROY: (id) => `/core-module/employee/api/department/${id}/`,
        },
        LOCATIONS: {
            INDEX: '/core-module/employee/api/location/',
            STORE: '/core-module/employee/api/location/',
            SHOW: (id) => `/core-module/employee/api/location/${id}/`,
            UPDATE: (id) => `/core-module/employee/api/location/${id}/`,
            DESTROY: (id) => `/core-module/employee/api/location/${id}/`,
        },
        DESIGNATIONS: {
            INDEX: '/core-module/employee/api/designation/',
            STORE: '/core-module/employee/api/designation/',
            SHOW: (id) => `/core-module/employee/api/designation/${id}/`,
            UPDATE: (id) => `/core-module/employee/api/designation/${id}/`,
            DESTROY: (id) => `/core-module/employee/api/designation/${id}/`,
        },
        EMPLOYEES: {
            INDEX: '/core-module/employee/api/employee/',
            STORE: '/core-module/employee/api/employee/',
            SHOW: (id) => `/core-module/employee/api/employee/${id}/`,
            UPDATE: (id) => `/core-module/employee/api/employee/${id}/`,
            DESTROY: (id) => `/core-module/employee/api/employee/${id}/`,
            STATS: '/core-module/employee/api/employee/stats/',
        },
        DOCUMENTS: {
            INDEX: '/core-module/employee/api/document/',
            STORE: '/core-module/employee/api/document/',
            SHOW: (id) => `/core-module/employee/api/document/${id}/`,
        },
    },

    /**
     * @namespace TALENT_GROWTH
     * @description Talent growth modules - engagement, performance, training, talent.
     * @see talent_growth/routes/
     * @routePrefix talent-growth
     */
    TALENT_GROWTH: {
        /** @routePrefix talent-growth.engagement */
        ENGAGEMENT: {
            SURVEYS: {
                INDEX: '/talent-growth/engagement/api/survey/',
                STORE: '/talent-growth/engagement/api/survey/',
                SHOW: (id) => `/talent-growth/engagement/api/survey/${id}/`,
                UPDATE: (id) => `/talent-growth/engagement/api/survey/${id}/`,
                DESTROY: (id) => `/talent-growth/engagement/api/survey/${id}/`,
            },
            RECOGNITION: {
                INDEX: '/talent-growth/engagement/api/recognition/',
                STORE: '/talent-growth/engagement/api/recognition/',
                SHOW: (id) => `/talent-growth/engagement/api/recognition/${id}/`,
                UPDATE: (id) => `/talent-growth/engagement/api/recognition/${id}/`,
                DESTROY: (id) => `/talent-growth/engagement/api/recognition/${id}/`,
                EMPLOYEE_POINTS: (employeeId) => `/talent-growth/engagement/api/recognition/${employeeId}/points/`,
            },
        },

        /** @routePrefix talent-growth.performance */
        PERFORMANCE: {
            REVIEWS: {
                INDEX: '/talent-growth/performance/api/review/',
                STORE: '/talent-growth/performance/api/review/',
                SHOW: (id) => `/talent-growth/performance/api/review/${id}/`,
                COMPLETE: (id) => `/talent-growth/performance/api/review/${id}/complete/`,
            },
            GOALS: {
                INDEX: '/talent-growth/performance/api/goal/',
                STORE: '/talent-growth/performance/api/goal/',
                SHOW: (id) => `/talent-growth/performance/api/goal/${id}/`,
                UPDATE_PROGRESS: (id) => `/talent-growth/performance/api/goal/${id}/progress/`,
            },
        },

        /** @routePrefix talent-growth.training */
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
                SHOW: (id) => `/talent-growth/training/api/enrollment/${id}/`,
                COMPLETE: (id) => `/talent-growth/training/api/enrollment/${id}/complete/`,
                BULK: '/talent-growth/training/api/enrollment/bulk/',
            },
        },

        /** @routePrefix talent-growth.talent */
        TALENT: {
            PROFILES: {
                INDEX: '/talent-growth/talent/api/profile/',
                STORE: '/talent-growth/talent/api/profile/',
                SHOW: (id) => `/talent-growth/talent/api/profile/${id}/`,
                UPDATE: (id) => `/talent-growth/talent/api/profile/${id}/`,
                DESTROY: (id) => `/talent-growth/talent/api/profile/${id}/`,
            },
            SUCCESSION: {
                INDEX: '/talent-growth/talent/api/succession/',
                STORE: '/talent-growth/talent/api/succession/',
                SHOW: (id) => `/talent-growth/talent/api/succession/${id}/`,
                UPDATE: (id) => `/talent-growth/talent/api/succession/${id}/`,
                DESTROY: (id) => `/talent-growth/talent/api/succession/${id}/`,
            },
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
    BASE_URL: 'http://localhost:9003',
    TIMEOUT: 10000,
    HEADERS: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    },
};