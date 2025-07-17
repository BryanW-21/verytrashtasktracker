document.addEventListener("DOMContentLoaded", () => {
  const authForm = document.getElementById("authForm");
  const authButton = document.getElementById("authButton");
  const authError = document.getElementById("auth-error");
  const formTitle = document.getElementById("form-title");
  const registerFields = document.getElementById("register-fields");
  const toggleAuth = document.getElementById("toggleAuth");

  let isLogin = true;

  // Check if URL has ?register=true and switch to register mode automatically
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get("register") === "true") {
    isLogin = false;
  }

  // Function to update UI based on mode
  const updateAuthUI = () => {
    formTitle.textContent = isLogin ? "Login" : "Register";
    authButton.textContent = isLogin ? "Login" : "Register";
    registerFields.classList.toggle("hidden", isLogin);
    toggleAuth.textContent = isLogin ? "Register" : "Login";
    authError.textContent = ""; // Clear error message when switching modes
  };

  // Initialize UI with correct mode
  updateAuthUI();

  // Toggle between login and register mode
  toggleAuth.addEventListener("click", (event) => {
    event.preventDefault();
    isLogin = !isLogin;
    updateAuthUI();
  });

  authForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const username = document.getElementById("username")?.value.trim();

    if (!email || !password || (!isLogin && !username)) {
      authError.textContent = "All fields are required!";
      return;
    }

    try {
      const endpoint = isLogin ? "/login" : "/register";
      const requestBody = isLogin
        ? { email, password }
        : { username, email, password };

      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
      });

      const data = await response.json();

      if (response.ok) {
        if (isLogin) {
          localStorage.setItem("jwt_token", data.access_token);
          window.location.href = "/index_user";
        } else {
          alert("Registration successful! You can now log in.");
          toggleAuth.click(); // Switch back to login mode
        }
      } else {
        // Explicitly check for duplicate email or username errors
        if (data.error === "Email already registered") {
          authError.textContent =
            "This email is already in use. Try logging in instead.";
        } else if (data.error === "Username already taken") {
          authError.textContent =
            "This username is already taken. Please choose another one.";
        } else {
          authError.textContent = data.error || "Authentication failed!";
        }
      }
    } catch (error) {
      console.error("Authentication error:", error);
      authError.textContent = "Server error. Please try again.";
    }
  });
});
