const uname = document.querySelector('#usernameField');
const email = document.querySelector('#emailField');
const password = document.querySelector('#passwordField');

const feedBackArea = document.querySelector(".invalid_feedback");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");

const showPasswordToggle = document.querySelector(".showPasswordToggle");
const submitBtn = document.querySelector(".submit-btn");

uname.addEventListener('keyup', (e)=>{
    const username = e.target.value;
    console.log(username);
    usernameSuccessOutput.style.display = "block";
    usernameSuccessOutput.textContent = `Checking  ${username}`;
    uname.classList.remove("is-invalid");
    feedBackArea.style.display = "none";
  
    if(username.length > 0){
        fetch('/signup/validate-username', {
            body : JSON.stringify({username:username}),
            method : "POST",
        }).then(res => res.json())
          .then((data) => {
            console.log(data);
            usernameSuccessOutput.style.display = "none";
              if(data.username_error){
                usernameField.classList.add("is-invalid");
                usernameSuccessOutput.style.display = "none";
                feedBackArea.style.display = "block";
                feedBackArea.innerHTML = `<p>${data.username_error}</p>`;
                submitBtn.disabled = true;       
              }else {
                submitBtn.removeAttribute("disabled");
              }
          });
        }
})


email.addEventListener('keyup', (e)=>{
    const emailVal = e.target.value;
    
    email.classList.remove("is-invalid");
    emailFeedBackArea.style.display = "none";
    
  if (emailVal.length > 0) {
    fetch("/signup/validate-email",{
      body: JSON.stringify({ email: emailVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        if (data.email_error) {
          submitBtn.disabled = true;
          email.classList.add("is-invalid");
          emailFeedBackArea.style.display = "block";
          emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
        } else {
          submitBtn.removeAttribute("disabled");
        }
      });
    }
})

const handleToggleInput = (e) => {
    if (showPasswordToggle.textContent === "SHOW") {
      showPasswordToggle.textContent = "HIDE";
      passwordField.setAttribute("type", "text");
    } else {
      showPasswordToggle.textContent = "SHOW";
      passwordField.setAttribute("type", "password");
    }
  };
  
showPasswordToggle.addEventListener("click", handleToggleInput);
  