function verifyOTP() {
    const userOTP = document.getElementById("otpInput").value;
    const storedOTP = localStorage.getItem("otp");

    if (userOTP === storedOTP) {
        alert("Verification successful!");

        // Move to next page
        window.location.href = "dashboard.html";
    } else {
        alert("Incorrect code!");
    }
}

function tryAnotherWay() {
    window.location.href = "fpnumber.html";
}

