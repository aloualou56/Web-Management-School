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



function startScanner() {
    const qrCodeSuccessCallback = (decodedText, decodedResult) => {
        console.log(`QR Code detected: ${decodedText}`);
        
        const csrftoken = getCookie('csrftoken');
        console.log('CSRF Token:', csrftoken); 

        fetch('/people/check-attendance/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken, 
            },
            credentials: 'same-origin',
            body: new URLSearchParams({
                'text_input': decodedText
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.match) {
                alert(data.message);
            } else {
                alert('No match found.');
            }
        })
        .catch(error => console.error('Error:', error));
    };

    const html5QrCode = new Html5Qrcode("reader");

    html5QrCode.start(
        { facingMode: "environment" }, 
        {
            fps: 10, 
            qrbox: { width: 120, height: 120 }
        },
        qrCodeSuccessCallback
    ).catch(err => {
        console.error(`Unable to start scanning, error: ${err}`);
    });
}

window.addEventListener('load', startScanner);
