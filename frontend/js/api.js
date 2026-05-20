const BACKEND_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:3000'
    : 'https://grade-smart-website.onrender.com'; // Thay link Render của bạn tại đây nếu khác

const BASE_URL = `${BACKEND_URL}/api`;

const api = {
    BACKEND_URL,
    BASE_URL,
    get: async (endpoint) => {
        const token = localStorage.getItem('token');
        const response = await fetch(`${BASE_URL}${endpoint}`, {
            headers: {
                'Authorization': token ? `Bearer ${token}` : '',
                'Content-Type': 'application/json'
            }
        });
        if (!response.ok) {
            if (response.status === 401) {
                localStorage.removeItem('token');
                window.location.href = 'login.html';
            }
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || errorData.message || `API error: ${response.status}`);
        }
        return response.json();
    },

    post: async (endpoint, data, isMultipart = false) => {
        const token = localStorage.getItem('token');
        const headers = {
            'Authorization': token ? `Bearer ${token}` : ''
        };
        
        if (!isMultipart) {
            headers['Content-Type'] = 'application/json';
        }

        const response = await fetch(`${BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: headers,
            body: isMultipart ? data : JSON.stringify(data)
        });

        if (!response.ok) {
            if (response.status === 401) {
                localStorage.removeItem('token');
                window.location.href = 'login.html';
            }
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || errorData.message || `API error: ${response.status}`);
        }
        return response.json();
    },

    put: async (endpoint, data) => {
        const token = localStorage.getItem('token');
        const response = await fetch(`${BASE_URL}${endpoint}`, {
            method: 'PUT',
            headers: {
                'Authorization': token ? `Bearer ${token}` : '',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            if (response.status === 401) {
                localStorage.removeItem('token');
                window.location.href = 'login.html';
            }
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || errorData.message || `API error: ${response.status}`);
        }
        return response.json();
    },

    delete: async (endpoint) => {
        const token = localStorage.getItem('token');
        const response = await fetch(`${BASE_URL}${endpoint}`, {
            method: 'DELETE',
            headers: {
                'Authorization': token ? `Bearer ${token}` : '',
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            if (response.status === 401) {
                localStorage.removeItem('token');
                window.location.href = 'login.html';
            }
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || errorData.message || `API error: ${response.status}`);
        }
        return response.json();
    }
};

window.api = api;
