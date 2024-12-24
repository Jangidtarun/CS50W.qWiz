document.addEventListener('DOMContentLoaded', () => {
    console.log('script is loading');

    const email = document.getElementById('email')
    let verification_status = false

    const sendbtn = document.getElementById('send-otp-btn');
    sendbtn.addEventListener('click', () => {
        if (email.value === '') {
            email.classList.add('is-invalid')
        } else {
            email.classList.remove('is-invalid')
            sendbtn.disabled = true;
            send_email(email.value).then(data => {
                document.getElementById('message').innerHTML = data.message
                time_remaining = 10
                intervalid = setInterval(() => {
                    time_remaining--;
                    if (time_remaining <= 0) {
                        clearInterval(intervalid)
                        if (!verification_status) {
                            document.getElementById('message').innerHTML = ''
                            sendbtn.disabled = false
                        }
                    }
                }, 1000);
            })
            vbtn.disabled = false;
        }
    })

    const otpinput = document.getElementById('otp')

    const vbtn = document.getElementById('verify-btn');
    vbtn.addEventListener('click', () => {
        if (otpinput.value === '') {
            otpinput.classList.add('is-invalid')
        } else {
            otpinput.classList.remove('is-invalid')
            verify_otp(email.value, otpinput.value).then(data => {
                document.getElementById('message').innerHTML = data.message
                if (data.pass) {
                    vbtn.disabled = true
                    otpinput.disabled = true
                    // email.disabled = true
                    time_remaining = 0
                    sendbtn.disabled = true
                    verification_status = true

                    document.getElementById('username').disabled = false;
                    document.getElementById('password').disabled = false;
                    document.getElementById('submit').disabled = false;
                }
            })
        }
    })
});

async function send_email(email_id) {
    const url = `/send-otp/${email_id}/`;
    const response = await fetch(url);
    const data = await response.json()
    return data
}

async function verify_otp(email_id, otp) {
    const url = `/verify-otp/${email_id}/${otp}/`
    const response = await fetch(url);
    const data = await response.json()
    return data
}

function getCSRFToken() {
    let cookieValue = null;
    const name = 'csrftoken';
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the CSRF token name?
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}