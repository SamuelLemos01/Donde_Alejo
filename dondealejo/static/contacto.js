


document.getElementById('contact-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const submitButton = this.querySelector('button[type=submit]')
    submitButton.classList.add('loading');


    const formData = new FormData(this);

    fetch('/send_email', {
        method: 'POST', 
        body: formData
    })

    .then(response => response.text())
    .then(data => {
        showFlashMessage('Mensaje enviado correctamente.', 'success');
        this.reset();
        submitButton.classList.remove('loading');
    });
});

function showFlashMessage(message, category) {
    const flashContainer = document.getElementById('flash-messages');
    const flashMessage = document.createElement('div');
    flashMessage.className = `alert ${category}`;
    flashMessage.textContent = message;

    flashContainer.appendChild(flashMessage);

    setTimeout(() => {
        flashMessage.remove();
    }, 5000);
}