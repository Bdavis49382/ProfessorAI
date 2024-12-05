
const chatBox = document.getElementById('chat-box');
chatBox.style.display = 'none';

document.getElementById('chat-button').addEventListener('click',() => {
    if (chatBox.classList.contains('d-block')) {
        chatBox.classList.remove('d-block');
        chatBox.classList.add('d-none');
    }
    else {
        chatBox.classList.remove('d-none');
        chatBox.classList.add('d-block');
    }
    // chatBox.style.display = chatBox.style.display == 'block' ? 'none' : '';
})

document.getElementById('request-button').addEventListener('click',() => {
    document.getElementById('loader').style.display = 'block';
})
