document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('form');
    const passwordInput = document.getElementById('password');
    const togglePasswordBtn = document.getElementById('togglePassword');
    const userBtn = document.getElementById('userBtn');
    
    // Toggle password visibility
    if (togglePasswordBtn) {
        togglePasswordBtn.addEventListener('click', () => {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            togglePasswordBtn.innerHTML = type === 'password' ? '<span class="material-symbols-outlined">visibility</span>' : '<span class="material-symbols-outlined">visibility_off</span>';
        });
    }
    
    // Quick login as user1
    if (userBtn) {
        userBtn.addEventListener('click', async () => {
            const usernameInput = document.getElementById('username');
            const submitBtn = loginForm.querySelector('button[type="submit"]');
            
            usernameInput.value = 'user1';
            passwordInput.value = '123456';
            
            submitBtn.click();
        });
    }
    
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const usernameInput = document.getElementById('username');
            const passwordInput = document.getElementById('password');
            const submitBtn = loginForm.querySelector('button[type="submit"]');
            
            const originalBtnText = submitBtn.innerText;
            submitBtn.innerText = 'Đang đăng nhập...';
            submitBtn.disabled = true;

            try {
                const response = await api.post('/auth/login', {
                    username: usernameInput.value,
                    password: passwordInput.value
                });

                if (response.token) {
                    localStorage.setItem('token', response.token);
                    localStorage.setItem('user', JSON.stringify(response.user));
                    window.location.href = 'dashboard.html';
                }
            } catch (error) {
                console.error('Login error:', error);
                alert('Đăng nhập thất bại: ' + error.message);
            } finally {
                submitBtn.innerText = originalBtnText;
                submitBtn.disabled = false;
            }
        });
    }
});
