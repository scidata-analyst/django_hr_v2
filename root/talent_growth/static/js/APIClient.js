/**
 * @class APIClient
 * @description REST API client for Laravel backend integration
 */
class APIClient {
    /**
     * Creates an instance of APIClient
     * @param {Object} config - Configuration object
     * @param {string} [config.baseURL=''] - Base URL of the API
     * @param {number} [config.timeout=10000] - Request timeout in milliseconds
     * @param {Object} [config.headers] - Default headers for all requests
     */
    constructor(config = {}) {
        this.baseURL = config.baseURL || '';
        this.timeout = config.timeout || 10000;
        this.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            ...config.headers
        };
    }

    /**
     * Sets authentication token
     * @param {string} token - Bearer token
     */
    setAuthToken(token) {
        this.headers['Authorization'] = `Bearer ${token}`;
    }

    /**
     * Gets endpoint URL
     * @param {string|Function} endpoint - Endpoint string or function
     * @param {Object} params - Parameters for dynamic endpoints
     * @returns {string} Full URL
     * @private
     */
    _getEndpoint(endpoint, params = {}) {
        if (typeof endpoint === 'function') {
            const arg = (params && params.id !== undefined) ? params.id : params;
            return endpoint(arg);
        }
        return endpoint;
    }

    /**
     * Internal request handler
     * @param {string} method - HTTP method
     * @param {string|Function} endpoint - API endpoint
     * @param {Object|null} data - Request payload
     * @param {Object} params - Route parameters
     * @returns {Promise<Object>} Response data
     * @private
     */
    async _request(method, endpoint, data = null, params = {}) {
        const urlPath = this._getEndpoint(endpoint, params);
        const url = `${this.baseURL}${urlPath}`;
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);

        const options = {
            method,
            headers: this.headers,
            signal: controller.signal,
            ...(data && { body: JSON.stringify(data) })
        };

        try {
            const response = await fetch(url, options);
            clearTimeout(timeoutId);

            if (!response.ok) {
                const contentType = response.headers.get('content-type') || '';
                if (contentType.includes('application/json')) {
                    const error = await response.json().catch(() => ({}));
                    throw new Error(error.message || error.error || `HTTP ${response.status}`);
                }
                const text = await response.text().catch(() => '');
                throw new Error(text || `HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            clearTimeout(timeoutId);
            throw error;
        }
    }

    /**
     * Retrieve all records
     * @param {string|Function} endpoint - API endpoint
     * @returns {Promise<Object>} All records
     */
    async all(endpoint) {
        return this._request('GET', endpoint);
    }

    /**
     * Display paginated listing with search and sort
     * @param {string|Function} endpoint - API endpoint
     * @param {Object} queryParams - Query parameters
     * @param {string} [queryParams.search=''] - Search keyword
     * @param {number} [queryParams.per_page=15] - Items per page
     * @param {string} [queryParams.sort_by='id'] - Sort column
     * @param {string} [queryParams.sort_direction='desc'] - Sort direction
     * @returns {Promise<Object>} Paginated records
     */
    async index(endpoint, queryParams = {}) {
        const { search = '', per_page = 15, sort_by = 'id', sort_direction = 'desc' } = queryParams;
        const query = new URLSearchParams({ search, per_page, sort_by, sort_direction }).toString();
        const urlPath = this._getEndpoint(endpoint);
        return this._request('GET', `${urlPath}?${query}`);
    }

    /**
     * Prepare data for creating new resource
     * @param {string|Function} endpoint - API endpoint
     * @returns {Promise<Object>} Create form data
     */
    async create(endpoint) {
        return this._request('GET', endpoint);
    }

    /**
     * Store newly created resource
     * @param {string|Function} endpoint - API endpoint
     * @param {Object} data - Resource data
     * @returns {Promise<Object>} Stored record
     */
    async store(endpoint, data) {
        return this._request('POST', endpoint, data);
    }

    /**
     * Display specified resource
     * @param {string|Function} endpoint - API endpoint
     * @param {number|string} id - Resource ID
     * @returns {Promise<Object>} Single record
     */
    async show(endpoint, id) {
        return this._request('GET', endpoint, null, { id });
    }

    /**
     * Prepare specified resource for editing
     * @param {string|Function} endpoint - API endpoint
     * @param {number|string} id - Resource ID
     * @returns {Promise<Object>} Edit form data
     */
    async edit(endpoint, id) {
        return this._request('GET', endpoint, null, { id });
    }

    /**
     * Update specified resource
     * @param {string|Function} endpoint - API endpoint
     * @param {number|string} id - Resource ID
     * @param {Object} data - Updated data
     * @returns {Promise<Object>} Updated record
     */
    async update(endpoint, id, data) {
        return this._request('PUT', endpoint, data, { id });
    }

    /**
     * Remove specified resource
     * @param {string|Function} endpoint - API endpoint
     * @param {number|string} id - Resource ID
     * @returns {Promise<Object>} Deletion response
     */
    async destroy(endpoint, id) {
        return this._request('DELETE', endpoint, null, { id });
    }
}