useremail = document.querySelector('#useremail')
feedback = document.querySelector('#feedback')
btn = document.getElementById('reset')

useremail.addEventListener('keyup' ,(e) => {
  btn.disabled = true;
    emailVal = e.target.value

    fetch("/signup/password-reset-email",{
      body: JSON.stringify({ email: emailVal }),
      method: "POST",
    })
    .then((res) => {
      console.log(emailVal);
      return res.json();
    })
    .then((data) => {
      console.log("data", data);
      if (data.email_error) {
        btn.disabled = true;
        feedback.innerHTML = `<p>${data.email_error}</p>`;
      } else {
        btn.disabled = false;
        btn.removeAttribute("disabled");
      }
    });
    
    })

     