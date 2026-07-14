const API_BASE_URL = 'http://localhost:8000';

// Check if user is logged in on page load
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    showHome();
});

// Check authentication status
function checkAuth() {
    const token = localStorage.getItem('admin_token');
    const adminLinks = document.getElementById('adminLinks');
    const loginLink = document.getElementById('loginLink');
    
    if (token) {
        adminLinks.style.display = 'inline';
        loginLink.style.display = 'none';
    } else {
        adminLinks.style.display = 'none';
        loginLink.style.display = 'inline';
    }
}

// Navigation Functions
function hideAllPages() {
    document.getElementById('homePage').style.display = 'none';
    document.getElementById('articlePage').style.display = 'none';
    document.getElementById('loginPage').style.display = 'none';
    document.getElementById('createPage').style.display = 'none';
    document.getElementById('editPage').style.display = 'none';
    document.getElementById('dashboardPage').style.display = 'none';
}

function showHome() {
    hideAllPages();
    document.getElementById('homePage').style.display = 'block';
    loadArticles();
}

function showLogin() {
    hideAllPages();
    document.getElementById('loginPage').style.display = 'block';
}

function showDashboard() {
    hideAllPages();
    document.getElementById('dashboardPage').style.display = 'block';
    loadDashboard();
}

function showCreateArticle() {
    hideAllPages();
    document.getElementById('createPage').style.display = 'block';
}

function showEditArticle(id) {
    hideAllPages();
    document.getElementById('editPage').style.display = 'block';
    loadArticleForEdit(id);
}

// API Functions
async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem('admin_token');
    
    const config = {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...(token && { 'admin_token': token }),
            ...options.headers,
        },
    };
    
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
    
    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Request failed' }));
        throw new Error(error.detail || 'Request failed');
    }
    
    return response.json();
}

// Load all articles for home page
async function loadArticles() {
    const container = document.getElementById('articlesList');
    container.innerHTML = '<div class="loading">Loading articles...</div>';
    
    try {
        const articles = await apiRequest('/articles');
        
        if (articles.length === 0) {
            container.innerHTML = '<p>No articles yet.</p>';
            return;
        }
        
        container.innerHTML = articles.map(article => `
            <div class="article-card" onclick="viewArticle(${article.id})">
                <h3>${article.title}</h3>
                <p class="date">${new Date(article.published_date).toLocaleDateString()}</p>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = `<div class="error">Failed to load articles: ${error.message}</div>`;
    }
}

// View single article
async function viewArticle(id) {
    hideAllPages();
    document.getElementById('articlePage').style.display = 'block';
    
    try {
        const article = await apiRequest(`/articles/${id}`);
        
        document.getElementById('articleTitle').textContent = article.title;
        document.getElementById('articleDate').textContent = 
            `Published: ${new Date(article.published_date).toLocaleDateString()} | Visits: ${article.visits}`;
        document.getElementById('articleContent').textContent = article.content;
    } catch (error) {
        alert(`Failed to load article: ${error.message}`);
        showHome();
    }
}

// Login
async function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('loginError');
    
    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });
        
        if (!response.ok) {
            throw new Error('Invalid credentials');
        }
        
        const token = await response.text();
        localStorage.setItem('admin_token', token);
        
        checkAuth();
        showDashboard();
        
        // Clear form
        document.getElementById('username').value = '';
        document.getElementById('password').value = '';
        errorDiv.style.display = 'none';
    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.style.display = 'block';
    }
}

// Logout
function logout() {
    localStorage.removeItem('admin_token');
    checkAuth();
    showHome();
}

// Create article
async function handleCreateArticle(event) {
    event.preventDefault();
    
    const title = document.getElementById('articleTitleInput').value;
    const content = document.getElementById('articleContentInput').value;
    const errorDiv = document.getElementById('createError');
    
    try {
        await apiRequest('/articles', {
            method: 'POST',
            body: JSON.stringify({ title, content }),
        });
        
        // Clear form
        document.getElementById('articleTitleInput').value = '';
        document.getElementById('articleContentInput').value = '';
        errorDiv.style.display = 'none';
        
        showDashboard();
    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.style.display = 'block';
    }
}

// Load article for editing
async function loadArticleForEdit(id) {
    try {
        const article = await apiRequest(`/articles/${id}`);
        
        document.getElementById('editArticleId').value = id;
        document.getElementById('editTitleInput').value = article.title;
        document.getElementById('editContentInput').value = article.content;
    } catch (error) {
        alert(`Failed to load article: ${error.message}`);
        showDashboard();
    }
}

// Edit article
async function handleEditArticle(event) {
    event.preventDefault();
    
    const id = document.getElementById('editArticleId').value;
    const title = document.getElementById('editTitleInput').value;
    const content = document.getElementById('editContentInput').value;
    const errorDiv = document.getElementById('editError');
    
    try {
        await apiRequest(`/articles/${id}`, {
            method: 'PATCH',
            body: JSON.stringify({ title, content }),
        });
        
        showDashboard();
    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.style.display = 'block';
    }
}

// Delete article
async function deleteArticle(id) {
    if (!confirm('Are you sure you want to delete this article?')) {
        return;
    }
    
    try {
        await apiRequest(`/articles/${id}`, {
            method: 'DELETE',
        });
        
        loadDashboard();
    } catch (error) {
        alert(`Failed to delete article: ${error.message}`);
    }
}

// Load admin dashboard
async function loadDashboard() {
    const tbody = document.getElementById('dashboardTable');
    tbody.innerHTML = '<tr><td colspan="5" class="loading">Loading...</td></tr>';
    
    try {
        const articles = await apiRequest('/admin/dashboard');
        
        if (articles.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5">No articles yet.</td></tr>';
            return;
        }
        
        tbody.innerHTML = articles.map(article => `
            <tr>
                <td>${article.id}</td>
                <td>${article.title}</td>
                <td>${new Date(article.published_date).toLocaleDateString()}</td>
                <td>${article.visits}</td>
                <td>
                    <button onclick="showEditArticle(${article.id})" class="btn btn-primary btn-small">Edit</button>
                    <button onclick="deleteArticle(${article.id})" class="btn btn-danger btn-small">Delete</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="5" class="error">Failed to load dashboard: ${error.message}</td></tr>`;
    }
}