document.querySelector(".login-btn").addEventListener("click", () => {
    login();
});

// Example: get selected features
const checkboxes = document.querySelectorAll(".features input");

checkboxes.forEach(box => {
    box.addEventListener("change", () => {
        console.log(box.parentElement.innerText, box.checked);
    });
});

//Login function
function login() {
    let email = document.getElementById("email").value;
    let pass = document.getElementById("password").value;

    if (email && pass) {
        alert("Login successful!");
        window.location.href = "index.html";
    } else {
        alert("Please enter email and password.");
    }
}

/* Signup function */

ddocument.addEventListener("DOMContentLoaded", function () {

  const signupBtn = document.getElementById("signupBtn");

  signupBtn.addEventListener("click", function () {

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!name || !email || !phone || !password) {
      alert("Please fill all fields!");
      return;
    }

    // Change button to green
    signupBtn.classList.add("success");
    signupBtn.textContent = "Success ✓";

  });

});

