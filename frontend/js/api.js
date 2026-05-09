const BASE_URL = 'http://localhost:3000/api';

const api = {
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
            throw new Error(`API error: ${response.status}`);
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
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `API error: ${response.status}`);
        }
        return response.json();
    }
};

window.api = api;
