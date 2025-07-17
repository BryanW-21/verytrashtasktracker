document.addEventListener("DOMContentLoaded", async () => {
  const menuToggle = document.querySelector(".menu-toggle");
  const navLinks = document.querySelector(".nav-links");

  if (menuToggle && navLinks) {
    menuToggle.addEventListener("click", () => {
      // Toggle visibility on small screens
      navLinks.style.display =
        navLinks.style.display === "flex" ? "none" : "flex";
    });

    // Ensure nav-links reappear when screen is resized to larger screens
    window.addEventListener("resize", () => {
      if (window.innerWidth > 768) {
        navLinks.style.display = "flex"; // Reset for larger screens
      }
    });
  }

  const taskForm = document.getElementById("task-form");
  const submitButton = document.querySelector(".cta.primary");

  // Prevent errors if the form is not found
  if (!taskForm || !submitButton) {
    console.error(
      "Error: Task form or submit button not found. Ensure you're on create_task.html."
    );
    return;
  }

  // Animation on form load
  const formContainer = document.querySelector(".task-form-container");
  if (formContainer) {
    formContainer.style.opacity = 0;
    formContainer.style.transform = "translateY(20px)";
    setTimeout(() => {
      formContainer.style.transition =
        "opacity 0.5s ease-out, transform 0.5s ease-out";
      formContainer.style.opacity = 1;
      formContainer.style.transform = "translateY(0)";
    }, 200);
  }

  // Button animation on hover
  submitButton.addEventListener("mouseover", () => {
    submitButton.style.transform = "scale(1.05)";
    submitButton.style.boxShadow = "0 4px 8px rgba(47, 128, 237, 0.3)";
  });

  submitButton.addEventListener("mouseout", () => {
    submitButton.style.transform = "scale(1)";
    submitButton.style.boxShadow = "none";
  });

  // Logout button
  const logoutBtn = document.getElementById("logout-btn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", (event) => {
      event.preventDefault(); // Prevent default link behavior
      localStorage.removeItem("jwt_token"); // Clear JWT from local storage
      window.location.href = "home.html"; // Redirect to home
    });
  }

  const pointsSlider = document.getElementById("points");
  const pointsValue = document.getElementById("points-value");

  if (pointsSlider && pointsValue) {
    // Update value dynamically as user moves the slider
    pointsSlider.addEventListener("input", () => {
      pointsValue.textContent = pointsSlider.value;
      updateSliderBackground(pointsSlider);
    });

    // Initialize slider appearance
    updateSliderBackground(pointsSlider);
  }

  // Function to update slider background based on progress
  function updateSliderBackground(slider) {
    const percentage = slider.value;
    slider.style.background = `linear-gradient(to right, #2f80ed ${percentage}%, #ddd ${percentage}%)`;
  }

  const formTitle = document.getElementById("form-title");
  const pageTitle = document.getElementById("page-title");

  // Get taskId from URL (if editing)
  const urlParams = new URLSearchParams(window.location.search);
  const taskId = urlParams.get("taskId");

  if (taskId) {
    // If editing, change form text
    formTitle.textContent = "Edit Task";
    pageTitle.textContent = "Edit Task";
    submitButton.textContent = "Update Task";

    try {
      const token = localStorage.getItem("jwt_token");
      if (!token) {
        alert("Unauthorized: Please log in first.");
        window.location.href = "login_register.html";
        return;
      }

      // Fetch task data
      const response = await fetch(
        `http://127.0.0.1:5000/api/tasks/${taskId}`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const task = await response.json();
      if (response.ok) {
        document.getElementById("task-id").value = task.taskId;
        document.getElementById("task-name").value = task.name;
        document.getElementById("description").value = task.description;
        document.getElementById("points").value = task.points;
        document.getElementById("image-url").value = task.image_url || "";
      } else {
        alert(`Error: ${task.error || "Failed to load task data"}`);
      }
    } catch (error) {
      console.error("Error fetching task data:", error);
      alert("An error occurred while loading the task.");
    }
  }

  // Handle form submission
  taskForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const taskName = document.getElementById("task-name").value.trim();
    const description = document.getElementById("description").value.trim();
    const points = document.getElementById("points").value.trim();
    const imageUrl = document.getElementById("image-url").value.trim();
    const taskIdValue = document.getElementById("task-id").value;

    const token = localStorage.getItem("jwt_token");

    if (!taskName || !description || !points) {
      alert("Please fill in all required fields.");
      return;
    }

    const requestBody = {
      name: taskName,
      description: description,
      points: parseInt(points, 10),
      image_url: imageUrl || null,
    };

    const requestOptions = {
      method: taskIdValue ? "PUT" : "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(requestBody),
    };

    const url = taskIdValue
      ? `http://127.0.0.1:5000/api/tasks/${taskIdValue}`
      : "http://127.0.0.1:5000/api/tasks";

    try {
      const response = await fetch(url, requestOptions);
      const data = await response.json();

      if (response.ok) {
        alert(
          taskIdValue
            ? "Task updated successfully!"
            : "Task created successfully!"
        );
        window.location.href = "/tasks";
      } else {
        alert(`Error: ${data.error || "Operation failed!"}`);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred.");
    }
  });
});
