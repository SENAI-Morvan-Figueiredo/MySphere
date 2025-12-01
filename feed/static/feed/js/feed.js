// Get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Like post functionality
document.querySelectorAll('.like-btn').forEach(button => {
    button.addEventListener('click', function(e) {
        e.preventDefault();
        const postId = this.dataset.postId;
        
        fetch(`/post/${postId}/like/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            const postCard = document.querySelector(`[data-post-id="${postId}"]`);
            const likesCount = postCard.querySelector('.likes-count');
            likesCount.textContent = data.total_likes;
            
            if (data.liked) {
                this.classList.add('liked');
            } else {
                this.classList.remove('liked');
            }
        })
        .catch(error => console.error('Error:', error));
    });
});

// Share post functionality
document.querySelectorAll('.share-btn').forEach(button => {
    button.addEventListener('click', function(e) {
        e.preventDefault();
        const postId = this.dataset.postId;
        
        fetch(`/post/${postId}/share/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            const postCard = document.querySelector(`[data-post-id="${postId}"]`);
            const sharesCount = postCard.querySelector('.shares-count');
            sharesCount.textContent = data.total_shares;
            
            alert('Post compartilhado com sucesso!');
        })
        .catch(error => console.error('Error:', error));
    });
});

// Comment form submission
document.querySelectorAll('.comment-form').forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const postId = this.dataset.postId;
        const conteudo = this.querySelector('input[name="conteudo"]').value;
        
        if (!conteudo.trim()) return;
        
        fetch(`/post/${postId}/comment/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `conteudo=${encodeURIComponent(conteudo)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const commentsList = this.closest('.comments-section').querySelector('.comments-list');
                const newComment = document.createElement('div');
                newComment.className = 'comment';
                newComment.innerHTML = `
                    <div class="comment-author">
                        <div class="user-avatar-tiny default-avatar">${data.comment.user.charAt(0).toUpperCase()}</div>
                    </div>
                    <div class="comment-content">
                        <h5>${data.comment.user}</h5>
                        <p>${data.comment.conteudo}</p>
                        <span class="comment-time">${data.comment.criado_em}</span>
                    </div>
                `;
                commentsList.appendChild(newComment);
                
                const postCard = document.querySelector(`[data-post-id="${postId}"]`);
                const commentsCount = postCard.querySelector('.comments-count');
                commentsCount.textContent = data.total_comments;
                
                this.querySelector('input[name="conteudo"]').value = '';
            }
        })
        .catch(error => console.error('Error:', error));
    });
});

// Toggle comment box
function toggleCommentBox(postId) {
    const commentsSection = document.getElementById(`comments-${postId}`);
    if (commentsSection.style.display === 'none') {
        commentsSection.style.display = 'block';
    } else {
        commentsSection.style.display = 'none';
    }
}

// Media preview (Image/Video)
document.getElementById('imagem-upload')?.addEventListener('change', function(e) {
    const file = e.target.files[0];
    const previewDiv = document.getElementById('media-preview');
    
    if (file) {
        const reader = new FileReader();
        
        reader.onload = function(event) {
            if (file.type.startsWith('image/')) {
                previewDiv.innerHTML = `
                    <div class="preview-container">
                        <img src="${event.target.result}" alt="Preview" class="preview-image">
                        <button type="button" class="remove-preview" onclick="removePreview('imagem')">✕</button>
                    </div>
                `;
            } else if (file.type.startsWith('video/')) {
                previewDiv.innerHTML = `
                    <div class="preview-container">
                        <video class="preview-video" controls>
                            <source src="${event.target.result}" type="${file.type}">
                        </video>
                        <button type="button" class="remove-preview" onclick="removePreview('imagem')">✕</button>
                    </div>
                `;
            }
            previewDiv.style.display = 'block';
        };
        
        reader.readAsDataURL(file);
    }
});

// File attachment preview
document.getElementById('arquivo-upload')?.addEventListener('change', function(e) {
    const file = e.target.files[0];
    const previewDiv = document.getElementById('media-preview');
    
    if (file) {
        previewDiv.innerHTML = `
            <div class="preview-container file-preview">
                <span class="icon">📎</span>
                <span class="file-name">${file.name}</span>
                <button type="button" class="remove-preview" onclick="removePreview('arquivo')">✕</button>
            </div>
        `;
        previewDiv.style.display = 'block';
    }
});

// Remove preview
function removePreview(type) {
    const previewDiv = document.getElementById('media-preview');
    const inputId = type === 'arquivo' ? 'arquivo-upload' : 'imagem-upload';
    const inputElement = document.getElementById(inputId);
    
    if (inputElement) {
        inputElement.value = '';
    }
    
    previewDiv.innerHTML = '';
    previewDiv.style.display = 'none';
}

// Autocompletar para @ e #
let autocompleteDiv = null;

function createAutocompleteDiv() {
    if (!autocompleteDiv) {
        autocompleteDiv = document.createElement('div');
        autocompleteDiv.id = 'autocomplete-suggestions';
        autocompleteDiv.style.cssText = `
            position: absolute;
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            max-height: 200px;
            overflow-y: auto;
            z-index: 1000;
            display: none;
            min-width: 200px;
        `;
        document.body.appendChild(autocompleteDiv);
    }
    return autocompleteDiv;
}

function showAutocompleteSuggestions(textarea, suggestions, type) {
    const div = createAutocompleteDiv();
    div.innerHTML = '';
    
    if (suggestions.length === 0) {
        div.style.display = 'none';
        return;
    }
    
    suggestions.forEach(item => {
        const suggestionItem = document.createElement('div');
        suggestionItem.style.cssText = `
            padding: 10px 15px;
            cursor: pointer;
            transition: background 0.2s;
        `;
        suggestionItem.onmouseover = () => suggestionItem.style.background = '#f0f0f0';
        suggestionItem.onmouseout = () => suggestionItem.style.background = 'white';
        
        if (type === 'mention') {
            suggestionItem.innerHTML = `<strong>@${item.username}</strong><br><small>${item.name || ''}</small>`;
            suggestionItem.onclick = () => insertSuggestion(textarea, `@${item.username} `);
        } else if (type === 'hashtag') {
            suggestionItem.innerHTML = `<strong>#${item.tag}</strong><br><small>${item.count || 0} posts</small>`;
            suggestionItem.onclick = () => insertSuggestion(textarea, `#${item.tag} `);
        }
        
        div.appendChild(suggestionItem);
    });
    
    const rect = textarea.getBoundingClientRect();
    div.style.top = `${rect.bottom + window.scrollY}px`;
    div.style.left = `${rect.left + window.scrollX}px`;
    div.style.display = 'block';
}

function insertSuggestion(textarea, text) {
    const value = textarea.value;
    const cursorPos = textarea.selectionStart;
    
    let start = cursorPos - 1;
    while (start >= 0 && value[start] !== ' ' && value[start] !== '\n') {
        start--;
    }
    start++;
    
    textarea.value = value.substring(0, start) + text + value.substring(cursorPos);
    textarea.focus();
    textarea.setSelectionRange(start + text.length, start + text.length);
    
    const div = createAutocompleteDiv();
    div.style.display = 'none';
}

// Detect hashtags and mentions in real-time with autocomplete
document.querySelector('textarea[name="conteudo"]')?.addEventListener('input', function(e) {
    const text = e.target.value;
    const cursorPos = e.target.selectionStart;
    
    let currentWord = '';
    let start = cursorPos - 1;
    while (start >= 0 && text[start] !== ' ' && text[start] !== '\n') {
        currentWord = text[start] + currentWord;
        start--;
    }
    
    if (currentWord.startsWith('@')) {
        const query = currentWord.substring(1);
        if (query.length >= 1) {
            fetch(`/feed/autocomplete/?type=user&q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => showAutocompleteSuggestions(e.target, data, 'mention'))
                .catch(() => {});
        }
    } else if (currentWord.startsWith('#')) {
        const query = currentWord.substring(1);
        if (query.length >= 1) {
            fetch(`/feed/autocomplete/?type=hashtag&q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => showAutocompleteSuggestions(e.target, data, 'hashtag'))
                .catch(() => {});
        }
    } else {
        const div = createAutocompleteDiv();
        div.style.display = 'none';
    }
});

// Fechar autocomplete ao clicar fora
document.addEventListener('click', function(e) {
    const div = createAutocompleteDiv();
    if (e.target.tagName !== 'TEXTAREA' && !div.contains(e.target)) {
        div.style.display = 'none';
    }
});

// Busca inteligente com delay
let searchTimeout;
const searchInput = document.querySelector('.search-bar input[name="q"]');

if (searchInput) {
    searchInput.addEventListener('input', function(e) {
        clearTimeout(searchTimeout);
        const query = e.target.value.trim();
        
        if (query.length < 2) return;
        
        searchTimeout = setTimeout(() => {
            // A busca será feita através do form submit normal
            console.log('Buscando:', query);
        }, 500);
    });
}


document.addEventListener("DOMContentLoaded", function () {
    const chatContainer = document.getElementById("chat-list-container");
    if (!chatContainer) return;

    function atualizarChats() {
        fetch(chatContainer.dataset.url)
            .then(response => {
                if (!response.ok) throw new Error("Erro na resposta");
                return response.text();
            })
            .then(html => {
                // Atualiza o conteúdo
                chatContainer.innerHTML = html;

                // Efeito suave de atualização
                chatContainer.style.opacity = "0.3";
                setTimeout(() => {
                    chatContainer.style.transition = "opacity 0.5s";
                    chatContainer.style.opacity = "1";
                }, 100);
            })
            .catch(err => console.error("Erro ao atualizar chats:", err));
    }

    // Atualiza a cada 5 segundos
    setInterval(atualizarChats, 1000);
});

function createPostHTML(p) {
    return `
    <article class="post-card" data-post-id="${p.id}">
        <div class="post-header">
            <div class="post-author">
                ${p.user.foto ? `
                    <img src="${p.user.foto}" class="user-avatar-small">
                ` : `
                    <div class="user-avatar-small default-avatar">${p.user.username[0].toUpperCase()}</div>
                `}
                <div class="author-info">
                    <a href="/perfil/${p.user.id}">
                        <h4>${p.user.nome}</h4>
                    </a>
                    <p class="post-time">${p.criado_em}</p>
                </div>
            </div>
            <button class="post-menu">⋮</button>
        </div>

        <div class="post-content">
            <p>${p.conteudo}</p>
        </div>

        ${p.imagem ? `
        <div class="post-media">
            <img src="${p.imagem}">
        </div>` : ''}

        ${p.video ? `
        <div class="post-media">
            <video controls>
                <source src="${p.video}">
            </video>
        </div>` : ''}

        ${p.arquivo ? `
        <div class="post-file">
            <a href="${p.arquivo}" download class="file-link">
                <span class="icon">📎</span> ${p.arquivo_nome}
            </a>
        </div>` : ''}

        <div class="post-stats">
            <span class="post-likes">
                ❤️ <span class="likes-count">${p.likes}</span> Like
            </span>
            <div class="post-interactions">
                <span><span class="comments-count">${p.comments}</span> Comment</span>
                <span><span class="shares-count">${p.shares}</span> Share</span>
            </div>
        </div>

        <div class="post-actions-bar">
            <button class="action-btn like-btn ${p.user_has_liked ? "liked" : ""}" data-post-id="${p.id}">
                <span class="icon">❤️</span> Like
            </button>
            <button class="action-btn comment-btn" onclick="toggleCommentBox(${p.id})">
                <span class="icon">💬</span> Comment
            </button>
            <button class="action-btn share-btn" data-post-id="${p.id}">
                <span class="icon">🔗</span> Share
            </button>
        </div>

        <div class="comments-section" id="comments-${p.id}" style="display:none">
            <div class="comments-list"></div>
            <form class="comment-form" data-post-id="${p.id}">
                <input type="text" name="conteudo" placeholder="Write a comment...">
                <button type="submit">Send</button>
            </form>
        </div>
    </article>`;
}


function startLongPolling() {
    const feedCenter = document.querySelector('.feed-center');
    if (!feedCenter) return;

    let latestPostId = feedCenter.dataset.latestPostId || 0;
    const checkUrl = `/check_new_posts/?last_post_id=${latestPostId}`;

    fetch(checkUrl, { method: 'GET' })
    .then(response => {
        if (!response.ok) throw new Error("Erro na resposta do Long Polling");
        return response.json();
    })
    .then(data => {

        if (data.status === 'updated') {
            console.log("NOVOS POSTS!");

            // Atualiza o último ID
            feedCenter.dataset.latestPostId = data.latest_post_id;

            const createPostCard = document.querySelector('.create-post-card');

            // Adiciona cada novo post no topo
            data.posts.forEach(p => {
                const postHTML = createPostHTML(p);

                const wrapper = document.createElement("div");
                wrapper.innerHTML = postHTML;

                createPostCard.insertAdjacentElement('afterend', wrapper.firstElementChild);
            });

            // remove msg "nenhum post"
            const noPosts = document.querySelector('.no-posts');
            if (noPosts) noPosts.remove();

            // reativar botões nos novos posts
            rebindPostEvents();
        }

        // sempre repete
        setTimeout(startLongPolling, 1000);

    })
    .catch(err => {
        console.error("Erro long polling:", err);
        setTimeout(startLongPolling, 5000);
    });
}


function likeHandler(e) {
    e.preventDefault();
    const postId = this.dataset.postId;

    fetch(`/post/${postId}/like/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(res => res.json())
    .then(data => {
        const card = document.querySelector(`[data-post-id="${postId}"]`);
        card.querySelector('.likes-count').textContent = data.total_likes;

        if (data.liked) this.classList.add("liked");
        else this.classList.remove("liked");
    });
}

function shareHandler(e) {
    e.preventDefault();
    const postId = this.dataset.postId;

    fetch(`/post/${postId}/share/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken }
    })
    .then(res => res.json())
    .then(data => {
        const card = document.querySelector(`[data-post-id="${postId}"]`);
        card.querySelector('.shares-count').textContent = data.total_shares;
    });
}

function commentHandler(e) {
    e.preventDefault();
    const postId = this.dataset.postId;
    const conteudo = this.querySelector("input").value;

    if (!conteudo.trim()) return;

    fetch(`/post/${postId}/comment/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `conteudo=${encodeURIComponent(conteudo)}`
    }).then(r => r.json()).then(data => {
        if (data.success) {
            const list = this.closest('.comments-section').querySelector('.comments-list');

            list.innerHTML += `
                <div class="comment">
                    <div class="comment-author">
                        <div class="user-avatar-tiny default-avatar">${data.comment.user[0].toUpperCase()}</div>
                    </div>
                    <div class="comment-content">
                        <h5>${data.comment.user}</h5>
                        <p>${data.comment.conteudo}</p>
                        <span class="comment-time">${data.comment.criado_em}</span>
                    </div>
                </div>
            `;

            const card = document.querySelector(`[data-post-id="${postId}"]`);
            card.querySelector('.comments-count').textContent = data.total_comments;

            this.querySelector("input").value = "";
        }
    });
}


document.addEventListener("DOMContentLoaded", function () {
    console.log("🚀 Iniciando long polling...");
    startLongPolling();
});