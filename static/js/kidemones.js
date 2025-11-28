function openKidemonaModal() {
    document.getElementById('kidemonaModal').style.display = 'flex';
}

function closeKidemonaModal() {
    document.getElementById('kidemonaModal').style.display = 'none';
    
    resetKidemonaForm(); 
}

function resetKidemonaForm() {
    const kidemonaForm = document.getElementById('kidemonaForm');
    kidemonaForm.reset();

    $('#mathites').val(''); 
    $('#mathites').trigger('chosen:updated');

    document.querySelector('#kidemonaModal h2').textContent = 'Προσθήκη Κηδεμόνα';
    document.querySelector('.modal-submit-btn').textContent = 'Προσθήκη';
}

document.getElementById('til').addEventListener('input', function() {
    this.value = this.value.replace(/[^0-9]/g, ''); 
});

document.getElementById('til_stath').addEventListener('input', function() {
    this.value = this.value.replace(/[^0-9]/g, ''); 
});

$(document).ready(function() {
    $('.chosen-select').chosen({
        placeholder_text_multiple: "Επιλέξτε Μαθητές",  
        no_results_text: "Δεν βρέθηκαν αποτελέσματα",     
        width: "100%"                                     
    });
});

document.getElementById('kidemonaForm').addEventListener('submit', function(event) {
    event.preventDefault(); 

    const kidemonaId = document.getElementById('kidemona_id').value;
    const url = kidemonaId ? `/kidemones/${kidemonaId}/update/` : '/Kidemones/'; 
    const method = kidemonaId ? 'POST' : 'POST'; 

    const formData = new FormData(this); 

    $.ajax({
        url: url,
        method: method,
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            closeKidemonaModal(); 
            
            location.reload();
        },
        error: function() {
            alert('An error occurred while saving'); 
        }
    });
});

function editKidemona(kidemonaId) {
    $.ajax({
        url: `/kidemones/${kidemonaId}/edit/`, 
        method: 'GET',
        success: function(kidemona) {
            populateKidemonaForm(kidemona); 
            openKidemonaModal(); 
        },
        error: function() {
            alert('Could not fetch data.'); 
        }
    });
}

function populateKidemonaForm(kidemona) {
    document.getElementById('kidemona_id').value = kidemona.id;
    document.getElementById('name_arx').value = kidemona.name_arx;
    document.getElementById('name_tel').value = kidemona.name_tel;
    document.getElementById('til').value = kidemona.til;
    document.getElementById('til_stath').value = kidemona.til_stath;
    document.getElementById('address').value = kidemona.address;
    document.getElementById('taxidr_code').value = kidemona.taxidr_code;
    document.getElementById('epagelma').value = kidemona.epagelma;
    document.getElementById('email').value = kidemona.email;

    $('#mathites').val(kidemona.mathites_ids);
    $('#mathites').trigger('chosen:updated');

    document.querySelector('#kidemonaModal h2').textContent = 'Επεξεργασία Κηδεμόνα';
    document.querySelector('.modal-submit-btn').textContent = 'Αποθήκευση';
}

function deleteKidemona(kidemonaId) {
    if (confirm('Are you sure you want to delete this?')) {
        
        $.ajax({
            url: `/kidemones/${kidemonaId}/delete/`,  
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken') 
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
