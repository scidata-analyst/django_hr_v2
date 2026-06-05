/**
 * @file constants.js
 * @description Centralized API endpoint constants.
 *              All routes are prefixed under `/api/v1` matching `routes/api/*.php`.
 */

/**
 * @constant {Object} API_ENDPOINTS
 * @description API endpoint URLs grouped by feature module.
 *              Static properties return a string; dynamic ones accept an `id` and return a string.
 */
const API_ENDPOINTS = {

    /**
     * @namespace APPEARANCE
     * @description Chatbot widget visual customization settings.
     * @see routes/api/appearance.php
     * @routePrefix api.v1.appearance
     */
    APPEARANCE: {
        INDEX: '/api/v1/appearance',
        STORE: '/api/v1/appearance',
        SHOW: (id) => `/api/v1/appearance/${id}`,
        UPDATE: (id) => `/api/v1/appearance/${id}`,
        DESTROY: (id) => `/api/v1/appearance/${id}`,
    },

    /**
     * @namespace CHAT
     * @description Chat conversations and messages.
     * @see routes/api/chat.php
     * @routePrefix api.v1.chat
     */
    CHAT: {
        /** @routePrefix api.v1.chat.conversations */
        CONVERSATIONS: {
            INDEX: '/api/v1/chat/conversations',
            STORE: '/api/v1/chat/conversations',
            SHOW: (id) => `/api/v1/chat/conversations/${id}`,
            UPDATE: (id) => `/api/v1/chat/conversations/${id}`,
            DESTROY: (id) => `/api/v1/chat/conversations/${id}`,
        },
        /** @routePrefix api.v1.chat.messages */
        MESSAGES: {
            INDEX: '/api/v1/chat/messages',
            STORE: '/api/v1/chat/messages',
            SHOW: (id) => `/api/v1/chat/messages/${id}`,
            UPDATE: (id) => `/api/v1/chat/messages/${id}`,
            DESTROY: (id) => `/api/v1/chat/messages/${id}`,
        },
    },

    /**
     * @namespace COMPLETION
     * @description Completion rules with conditions, responses, and flow designs.
     * @see routes/api/completion.php
     * @routePrefix api.v1.completions
     */
    COMPLETION: {
        INDEX: '/api/v1/completions',
        STORE: '/api/v1/completions',
        SHOW: (id) => `/api/v1/completions/${id}`,
        UPDATE: (id) => `/api/v1/completions/${id}`,
        DESTROY: (id) => `/api/v1/completions/${id}`,

        /** @routePrefix api.v1.completions.conditions */
        CONDITIONS: {
            INDEX: '/api/v1/completions/conditions',
            STORE: '/api/v1/completions/conditions',
            SHOW: (id) => `/api/v1/completions/conditions/${id}`,
            UPDATE: (id) => `/api/v1/completions/conditions/${id}`,
            DESTROY: (id) => `/api/v1/completions/conditions/${id}`,
        },
        /** @routePrefix api.v1.completions.responses */
        RESPONSES: {
            INDEX: '/api/v1/completions/responses',
            STORE: '/api/v1/completions/responses',
            SHOW: (id) => `/api/v1/completions/responses/${id}`,
            UPDATE: (id) => `/api/v1/completions/responses/${id}`,
            DESTROY: (id) => `/api/v1/completions/responses/${id}`,
        },
        /** @routePrefix api.v1.completions.flow-designs */
        FLOW_DESIGNS: {
            INDEX: '/api/v1/completions/flow-designs',
            STORE: '/api/v1/completions/flow-designs',
            SHOW: (id) => `/api/v1/completions/flow-designs/${id}`,
            UPDATE: (id) => `/api/v1/completions/flow-designs/${id}`,
            DESTROY: (id) => `/api/v1/completions/flow-designs/${id}`,
        },
    },

    /**
     * @namespace COMPONENT
     * @description Reusable UI components with configuration overrides.
     * @see routes/api/component.php
     * @routePrefix api.v1.components
     */
    COMPONENT: {
        INDEX: '/api/v1/components',
        STORE: '/api/v1/components',
        SHOW: (id) => `/api/v1/components/${id}`,
        UPDATE: (id) => `/api/v1/components/${id}`,
        DESTROY: (id) => `/api/v1/components/${id}`,

        /** @routePrefix api.v1.components.ui-components */
        UI_COMPONENTS: {
            INDEX: '/api/v1/components/ui-components',
            STORE: '/api/v1/components/ui-components',
            SHOW: (id) => `/api/v1/components/ui-components/${id}`,
            UPDATE: (id) => `/api/v1/components/ui-components/${id}`,
            DESTROY: (id) => `/api/v1/components/ui-components/${id}`,
        },
        /** @routePrefix api.v1.components.configs */
        CONFIGS: {
            INDEX: '/api/v1/components/configs',
            STORE: '/api/v1/components/configs',
            SHOW: (id) => `/api/v1/components/configs/${id}`,
            UPDATE: (id) => `/api/v1/components/configs/${id}`,
            DESTROY: (id) => `/api/v1/components/configs/${id}`,
        },
    },

    /**
     * @namespace CONTENT
     * @description Message templates, content templates, and quick replies.
     * @see routes/api/content.php
     * @routePrefix api.v1.content
     */
    CONTENT: {
        /** @routePrefix api.v1.content.message-templates */
        MESSAGE_TEMPLATES: {
            INDEX: '/api/v1/content/message-templates',
            STORE: '/api/v1/content/message-templates',
            SHOW: (id) => `/api/v1/content/message-templates/${id}`,
            UPDATE: (id) => `/api/v1/content/message-templates/${id}`,
            DESTROY: (id) => `/api/v1/content/message-templates/${id}`,
        },
        /** @routePrefix api.v1.content.content-templates */
        CONTENT_TEMPLATES: {
            INDEX: '/api/v1/content/content-templates',
            STORE: '/api/v1/content/content-templates',
            SHOW: (id) => `/api/v1/content/content-templates/${id}`,
            UPDATE: (id) => `/api/v1/content/content-templates/${id}`,
            DESTROY: (id) => `/api/v1/content/content-templates/${id}`,
        },
        /** @routePrefix api.v1.content.quick-replies */
        QUICK_REPLIES: {
            INDEX: '/api/v1/content/quick-replies',
            STORE: '/api/v1/content/quick-replies',
            SHOW: (id) => `/api/v1/content/quick-replies/${id}`,
            UPDATE: (id) => `/api/v1/content/quick-replies/${id}`,
            DESTROY: (id) => `/api/v1/content/quick-replies/${id}`,
        },
    },

    /**
     * @namespace DASHBOARD
     * @description Dashboard summary data and analytics widgets.
     * @see routes/api/dashboard.php
     * @routePrefix api.v1.dashboard
     */
    DASHBOARD: {
        INDEX: '/api/v1/dashboard',
        STORE: '/api/v1/dashboard',
        SHOW: (id) => `/api/v1/dashboard/${id}`,
        UPDATE: (id) => `/api/v1/dashboard/${id}`,
        DESTROY: (id) => `/api/v1/dashboard/${id}`,
    },

    /**
     * @namespace DICTIONARY
     * @description Dictionary word management including correct words and wrong-word variants.
     * @see routes/api/dictionary.php
     * @routePrefix api.v1.dictionary
     */
    DICTIONARY: {
        /** @routePrefix api.v1.dictionary.words */
        WORDS: {
            INDEX: '/api/v1/dictionary/words',
            STORE: '/api/v1/dictionary/words',
            SHOW: (id) => `/api/v1/dictionary/words/${id}`,
            UPDATE: (id) => `/api/v1/dictionary/words/${id}`,
            DESTROY: (id) => `/api/v1/dictionary/words/${id}`,
        },
        /** @routePrefix api.v1.dictionary.wrong-words */
        WRONG_WORDS: {
            INDEX: '/api/v1/dictionary/wrong-words',
            STORE: '/api/v1/dictionary/wrong-words',
            SHOW: (id) => `/api/v1/dictionary/wrong-words/${id}`,
            UPDATE: (id) => `/api/v1/dictionary/wrong-words/${id}`,
            DESTROY: (id) => `/api/v1/dictionary/wrong-words/${id}`,
        },
    },

    /**
     * @namespace FLOW
     * @description Chatbot conversation flows with nodes, connections, and flow designs.
     * @see routes/api/flow.php
     * @routePrefix api.v1.flows
     */
    FLOW: {
        INDEX: '/api/v1/flows',
        STORE: '/api/v1/flows',
        SHOW: (id) => `/api/v1/flows/${id}`,
        UPDATE: (id) => `/api/v1/flows/${id}`,
        DESTROY: (id) => `/api/v1/flows/${id}`,

        /** @routePrefix api.v1.flows.designs */
        DESIGNS: {
            INDEX: '/api/v1/flows/designs',
            STORE: '/api/v1/flows/designs',
            SHOW: (id) => `/api/v1/flows/designs/${id}`,
            UPDATE: (id) => `/api/v1/flows/designs/${id}`,
            DESTROY: (id) => `/api/v1/flows/designs/${id}`,
        },
        /** @routePrefix api.v1.flows.nodes */
        NODES: {
            INDEX: '/api/v1/flows/nodes',
            STORE: '/api/v1/flows/nodes',
            SHOW: (id) => `/api/v1/flows/nodes/${id}`,
            UPDATE: (id) => `/api/v1/flows/nodes/${id}`,
            DESTROY: (id) => `/api/v1/flows/nodes/${id}`,
        },
        /** @routePrefix api.v1.flows.connections */
        CONNECTIONS: {
            INDEX: '/api/v1/flows/connections',
            STORE: '/api/v1/flows/connections',
            SHOW: (id) => `/api/v1/flows/connections/${id}`,
            UPDATE: (id) => `/api/v1/flows/connections/${id}`,
            DESTROY: (id) => `/api/v1/flows/connections/${id}`,
        },
    },

    /**
     * @namespace INTEGRATION
     * @description Third-party integration records and configuration.
     * @see routes/api/integration.php
     * @routePrefix api.v1.integrations
     */
    INTEGRATION: {
        INDEX: '/api/v1/integrations',
        STORE: '/api/v1/integrations',
        SHOW: (id) => `/api/v1/integrations/${id}`,
        UPDATE: (id) => `/api/v1/integrations/${id}`,
        DESTROY: (id) => `/api/v1/integrations/${id}`,
    },

    /**
     * @namespace LANGUAGE_DETECTION
     * @description Language detection records and language rule definitions.
     * @see routes/api/language-detection.php
     * @routePrefix api.v1.language-detection
     */
    LANGUAGE_DETECTION: {
        INDEX: '/api/v1/language-detection',
        STORE: '/api/v1/language-detection',
        SHOW: (id) => `/api/v1/language-detection/${id}`,
        UPDATE: (id) => `/api/v1/language-detection/${id}`,
        DESTROY: (id) => `/api/v1/language-detection/${id}`,

        /** @routePrefix api.v1.language-detection.rules */
        RULES: {
            INDEX: '/api/v1/language-detection/rules',
            STORE: '/api/v1/language-detection/rules',
            SHOW: (id) => `/api/v1/language-detection/rules/${id}`,
            UPDATE: (id) => `/api/v1/language-detection/rules/${id}`,
            DESTROY: (id) => `/api/v1/language-detection/rules/${id}`,
        },
    },

    /**
     * @namespace NLP
     * @description Natural Language Processing — intents, entities, training phrases, and flows.
     * @see routes/api/nlp.php
     * @routePrefix api.v1.nlp
     */
    NLP: {
        /** @routePrefix api.v1.nlp.flows */
        FLOWS: {
            INDEX: '/api/v1/nlp/flows',
            STORE: '/api/v1/nlp/flows',
            SHOW: (id) => `/api/v1/nlp/flows/${id}`,
            UPDATE: (id) => `/api/v1/nlp/flows/${id}`,
            DESTROY: (id) => `/api/v1/nlp/flows/${id}`,
        },
        /** @routePrefix api.v1.nlp.intents */
        INTENTS: {
            INDEX: '/api/v1/nlp/intents',
            STORE: '/api/v1/nlp/intents',
            SHOW: (id) => `/api/v1/nlp/intents/${id}`,
            UPDATE: (id) => `/api/v1/nlp/intents/${id}`,
            DESTROY: (id) => `/api/v1/nlp/intents/${id}`,
        },
        /** @routePrefix api.v1.nlp.intent-entities */
        INTENT_ENTITIES: {
            INDEX: '/api/v1/nlp/intent-entities',
            STORE: '/api/v1/nlp/intent-entities',
            SHOW: (id) => `/api/v1/nlp/intent-entities/${id}`,
            UPDATE: (id) => `/api/v1/nlp/intent-entities/${id}`,
            DESTROY: (id) => `/api/v1/nlp/intent-entities/${id}`,
        },
        /** @routePrefix api.v1.nlp.training-phrases */
        TRAINING_PHRASES: {
            INDEX: '/api/v1/nlp/training-phrases',
            STORE: '/api/v1/nlp/training-phrases',
            SHOW: (id) => `/api/v1/nlp/training-phrases/${id}`,
            UPDATE: (id) => `/api/v1/nlp/training-phrases/${id}`,
            DESTROY: (id) => `/api/v1/nlp/training-phrases/${id}`,
        },
        /** @routePrefix api.v1.nlp.entities */
        ENTITIES: {
            INDEX: '/api/v1/nlp/entities',
            STORE: '/api/v1/nlp/entities',
            SHOW: (id) => `/api/v1/nlp/entities/${id}`,
            UPDATE: (id) => `/api/v1/nlp/entities/${id}`,
            DESTROY: (id) => `/api/v1/nlp/entities/${id}`,
        },
        /** @routePrefix api.v1.nlp.entity-values */
        ENTITY_VALUES: {
            INDEX: '/api/v1/nlp/entity-values',
            STORE: '/api/v1/nlp/entity-values',
            SHOW: (id) => `/api/v1/nlp/entity-values/${id}`,
            UPDATE: (id) => `/api/v1/nlp/entity-values/${id}`,
            DESTROY: (id) => `/api/v1/nlp/entity-values/${id}`,
        },
    },

    /**
     * @namespace SENTIMENT_ANALYSIS
     * @description Sentiment analysis records and sentiment rule definitions.
     * @see routes/api/sentiment-analysis.php
     * @routePrefix api.v1.sentiment-analysis
     */
    SENTIMENT_ANALYSIS: {
        INDEX: '/api/v1/sentiment-analysis',
        STORE: '/api/v1/sentiment-analysis',
        SHOW: (id) => `/api/v1/sentiment-analysis/${id}`,
        UPDATE: (id) => `/api/v1/sentiment-analysis/${id}`,
        DESTROY: (id) => `/api/v1/sentiment-analysis/${id}`,

        /** @routePrefix api.v1.sentiment-analysis.rules */
        RULES: {
            INDEX: '/api/v1/sentiment-analysis/rules',
            STORE: '/api/v1/sentiment-analysis/rules',
            SHOW: (id) => `/api/v1/sentiment-analysis/rules/${id}`,
            UPDATE: (id) => `/api/v1/sentiment-analysis/rules/${id}`,
            DESTROY: (id) => `/api/v1/sentiment-analysis/rules/${id}`,
        },
    },

    /**
     * @namespace SETTING
     * @description Chatbot runtime configuration settings.
     * @see routes/api/setting.php
     * @routePrefix api.v1.setting
     */
    SETTING: {
        INDEX: '/api/v1/setting',
        STORE: '/api/v1/setting',
        SHOW: (id) => `/api/v1/setting/${id}`,
        UPDATE: (id) => `/api/v1/setting/${id}`,
        DESTROY: (id) => `/api/v1/setting/${id}`,
    },

    /**
     * @namespace USER
     * @description CMS user accounts with role and status management.
     * @see routes/api/user.php
     * @routePrefix api.v1.users
     */
    USER: {
        INDEX: '/api/v1/users',
        STORE: '/api/v1/users',
        SHOW: (id) => `/api/v1/users/${id}`,
        UPDATE: (id) => `/api/v1/users/${id}`,
        DESTROY: (id) => `/api/v1/users/${id}`,
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
    BASE_URL: 'http://localhost:8000',
    TIMEOUT: 10000,
    HEADERS: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    },
};