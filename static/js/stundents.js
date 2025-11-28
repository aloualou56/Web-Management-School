function openStudentModal() {
    document.getElementById('studentModal').style.display = 'flex';
}

function closeStudentModal() {
    document.getElementById('studentModal').style.display = 'none';
    
    resetStudentForm(); 
}

function resetStudentForm() {
    const studentForm = document.getElementById('studentForm');
    studentForm.reset();

    $('#kidemones').val(''); 
    $('#kidemones').trigger('chosen:updated');

    document.querySelector('#studentModal h2').textContent = 'Προσθήκη Μαθητή';
    document.querySelector('.modal-submit-btn').textContent = 'Προσθήκη';
}

document.getElementById('foto').addEventListener('change', function() {
    const file = this.files[0];
    const fileChosen = document.getElementById('file-chosen');
    const imagePreviewDiv = document.getElementById('image-preview');
    const imagePreviewImg = document.getElementById('image-preview-img');
    
    if (file) {
        fileChosen.textContent = file.name;
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreviewImg.src = e.target.result;
            imagePreviewDiv.style.display = 'block'; 
        };
        reader.readAsDataURL(file);
    } else {
        fileChosen.textContent = 'No file chosen';
        imagePreviewDiv.style.display = 'none'; 
    }
});

document.getElementById('til').addEventListener('input', function() {
    this.value = this.value.replace(/[^0-9]/g, ''); 
});

$(document).ready(function() {
    $('.chosen-select').chosen({
        placeholder_text_multiple: "Επιλέξτε Κηδεμόνες",  
        no_results_text: "Δεν βρέθηκαν αποτελέσματα",     
        width: "100%"                                     
    });
});


document.getElementById('studentForm').addEventListener('submit', function(event) {
    event.preventDefault(); 

    const studentId = document.getElementById('student_id').value;
    const url = studentId ? `/students/${studentId}/update/` : '/students/'; 
    const method = studentId ? 'POST' : 'POST'; 

    const formData = new FormData(this); 

    $.ajax({
        url: url,
        method: method,
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            closeStudentModal(); 
            
            location.reload();
        },
        error: function() {
            alert('An error occurred while saving'); 
        }
    });
});

function editStudent(studentId) {
    $.ajax({
        url: `/students/${studentId}/edit/`, 
        method: 'GET',
        success: function(student) {
            populateStudentForm(student); 
            openStudentModal(); 
        },
        error: function() {
            alert('Could not fetch data'); 
        }
    });
}

function populateStudentForm(student) {
    document.getElementById('student_id').value = student.id;
    document.getElementById('name_arx').value = student.name_arx;
    document.getElementById('name_tel').value = student.name_tel;
    document.getElementById('til').value = student.til;
    document.getElementById('address').value = student.address;
    document.getElementById('School').value = student.School;
    document.getElementById('School_year').value = student.School_year;
    document.getElementById('birth_date').value = student.birth_date;
    document.getElementById('email').value = student.email;
    document.getElementById('taxh').value = student.taxh.id;
    document.getElementById('payment_plan').value = student.payment_plan ? student.payment_plan.id : '';
    
    $('#kidemones').val(student.kidemones_ids);
    $('#kidemones').trigger('chosen:updated');

    document.querySelector('#studentModal h2').textContent = 'Επεξεργασία Μαθητή';
    document.querySelector('.modal-submit-btn').textContent = 'Αποθήκευση';
}

function deleteStudent(studentId) {
    if (confirm('Are you sure you want to delete this student?')) {
        
        $.ajax({
            url: `/students/${studentId}/delete/`,  
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken') // prepei na uparxei alliws forbitten gia kapoion logo
            },
            success: function() {
                
                location.reload();
            },
            error: function() {
                alert('Failed to delete');
            }
        });
    }
}

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