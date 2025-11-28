
document.addEventListener('DOMContentLoaded', function() {
    const resetTimeInput = document.getElementById('reset_time');
    const currentTime = new Date().toISOString().slice(11, 16); 
    resetTimeInput.value = currentTime;  
});


const modal = document.getElementById('taxhModal');
const openModalButton = document.getElementById('openModal');
const closeModalButton = document.getElementsByClassName('close')[0];

openModalButton.onclick = function() {
    modal.style.display = 'block';
};

closeModalButton.onclick = function() {
    modal.style.display = 'none';
};

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
};


function toggleDeleteButton(checkbox) {
    const deleteButton = checkbox.nextElementSibling.nextElementSibling; 
    if (checkbox.checked) {
        deleteButton.style.display = 'none';
    } else {
        deleteButton.style.display = 'inline-block'; 
    }
}

function confirmDeletion(studentId) {
    if (confirm('Are you sure you want to remove this student from the class?')) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/removeFromClass/${studentId}/`;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'csrfmiddlewaretoken';
        input.value = csrfToken;
        form.appendChild(input);
        document.body.appendChild(form);
        form.submit();
    }
}

function toggleDeleteButton(checkbox) {
    const deleteButton = checkbox.closest('li').querySelector('.delete-confirm-button');
    deleteButton.style.display = checkbox.checked ? 'inline-block' : 'none';
}
