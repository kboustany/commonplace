function formModal(formId, bodyId) {
    const form = document.querySelector(`#${formId}`);
    if (!form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        const url = form.action;
        const formData = new FormData(form);

        fetch(url, {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect_url;
            } else {
                const body = document.querySelector(`#${bodyId}`);
                if (body) {
                    body.innerHTML = data.form_html;
                }
            }
        })
        .catch(error => console.error("Error:", error));        
    });
}


function searchBar({
    inputId,
    suggestionsBoxId,
    hiddenInputId,
    searchUrl,
    minLength = 2,
    debounceDelay = 250,
}) {
    const input = document.getElementById(inputId);
    const suggestionsBox = document.getElementById(suggestionsBoxId);
    const hiddenInput = document.getElementById(hiddenInputId);
    let timeout = null;

    if (!input || !suggestionsBox || !hiddenInput) return;

    input.addEventListener('input', function () {
        const query = input.value.trim();

        if (timeout) clearTimeout(timeout);
        if (query.length < minLength) {
            suggestionsBox.classList.add('d-none');
            return;
        }

        timeout = setTimeout(() => {
            fetch(`${searchUrl}?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                suggestionsBox.innerHTML = '';
                if (!data.length) {
                    suggestionsBox.classList.add('d-none');
                    return;
                }

                data.forEach(item => {
                    const option = document.createElement('button');
                    option.type = 'button';
                    option.classList.add('dropdown-item');
                    option.textContent = item.name;
                    option.dataset.id = item.id;
                    option.addEventListener('click', () => {
                        input.value = item.name;
                        hiddenInput.value = item.id;
                        suggestionsBox.classList.add('d-none');
                    });
                    suggestionsBox.appendChild(option);
                });

                suggestionsBox.classList.remove('d-none');
            });
        }, debounceDelay);
    });

    document.addEventListener('click', e => {
        if (!suggestionsBox.contains(e.target) && e.target !== input) {
            suggestionsBox.classList.add('d-none');
        }
    }); 
}