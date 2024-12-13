

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
})

document.getElementById('request-button').addEventListener('click',() => {
    document.getElementById('loader').style.display = 'block';
})

const codeBox = document.getElementById('code-box');
codeBox.addEventListener('keydown',(e) => {
    document.getElementById('saved').textContent = 'Your code is not saved.'
    if (e.key == 'Tab') {
        e.preventDefault();
        let start = codeBox.selectionStart;
        let end = codeBox.selectionEnd;

        // set textarea value to: text before caret + tab + text after caret
        codeBox.value = codeBox.value.substring(0, start) +
        "\t" + codeBox.value.substring(end);

        // put caret at right position again
        codeBox.selectionStart = codeBox.selectionEnd = start + 1;
    }
})

// hotkeys
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && e.key == 'Enter') {
        document.getElementById('submit-button').click();
    }
    else if (e.ctrlKey && e.key == 'Enter') {
        document.getElementById('run-button').click();
    }
    else if (e.ctrlKey && e.key == 's') {
        e.preventDefault();
        document.getElementById('save-button').click();
    }
})