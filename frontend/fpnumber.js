function continueAction() {
    const phone = document.getElementById("phone").value;

    if (phone === "") {
        alert("Please enter mobile number");
        return;
    }

    // Generate 5-digit OTP
    const otp = Math.floor(10000 + Math.random() * 90000);

    // Save OTP
    localStorage.setItem("otp", otp);
    localStorage.setItem("phone", phone);

    // Demo message
    alert("OTP sent to " + phone + "\nDemo OTP: " + otp);

    // Move to OTP page
    window.location.href = "otpn.html";
}

function searchByEmail() {
    alert("Email option coming soon");
}
