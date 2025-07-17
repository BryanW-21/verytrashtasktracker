document.querySelectorAll(".nav-links a").forEach((link) => {
  link.addEventListener("click", (e) => {
    // Prevent default anchor behavior
    e.preventDefault();

    // Get the target section from the href attribute
    const targetId = link.getAttribute("href");
    const targetSection = document.querySelector(targetId);

    if (targetSection) {
      // Calculate the scroll position with offset (e.g., 70px for header)
      const offset = 70; // Adjust as needed
      const targetPosition =
        targetSection.getBoundingClientRect().top + window.pageYOffset - offset;

      // Smooth scroll to the section
      window.scrollTo({
        top: targetPosition,
        behavior: "smooth",
      });
    }
  });
});

// Initialize
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

  // Get the current page's filename
  const currentPage = window.location.pathname.split("/").pop();
  // Handle Create Task Button (Redirect to Create Task Page)
  const createTaskBtn = document.querySelector('a[href="./create_task.html"]');
  if (createTaskBtn) {
    createTaskBtn.addEventListener("click", (event) => {
      event.preventDefault();
      window.location.href = "/create_task";
    });
  }

  // Handle Logout Button (Clear JWT and Redirect)
  const logoutBtn = document.getElementById("logout-btn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", (event) => {
      event.preventDefault(); // Prevent default link behavior
      localStorage.removeItem("jwt_token"); // Clear JWT
      alert("You have been logged out.");
      window.location.href = "/home"; // Redirect to home page
    });
  }

  // Function to determine points color
  const getPointsColor = (points) => {
    const maxPoints = 100;
    const normalizedPoints = Math.min(Math.max(points, 0), maxPoints); // Ensure within range

    // Gradual transition from Red (low points) → Yellow → Green (near 100)
    const red = Math.max(
      0,
      255 - Math.floor((normalizedPoints / maxPoints) * 255)
    );
    const green = Math.min(
      255,
      Math.floor((normalizedPoints / maxPoints) * 255)
    );

    return `rgb(${red}, ${green}, 0)`; // Returns dynamic color based on points
  };

  const loginBtn = document.getElementById("login-btn");

  if (loginBtn) {
    loginBtn.addEventListener("click", (event) => {
      event.preventDefault();
      console.log("click on login");
      window.location.href = "/login_register"; // Redirect to Login/Register page
    });
  }

  const startBtn = document.getElementById("start-btn");

  if (startBtn) {
    startBtn.addEventListener("click", (event) => {
      event.preventDefault();
      console.log("click on start");
      window.location.href = "/login_register?register=true"; // Redirect to Tasks page
    });
  }

  const taskContainer = document.getElementById("task-list");
  const searchBar = document.getElementById("search-bar");
  let allTasks = []; // Stores original task list

  // Function to fetch tasks from the API
  const fetchTasks = async () => {
    if (!window.location.pathname.includes("tasks")) return;
    try {
      const token = localStorage.getItem("jwt_token");

      if (!token) {
        alert("Unauthorized: Please log in first.");
        window.location.href = "/login_register"; // Redirect if not logged in
        return;
      }

      const response = await fetch("http://127.0.0.1:5000/api/tasks", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      allTasks = await response.json(); // Store all tasks in memory

      if (!response.ok) {
        alert(`Error: ${allTasks.error || "Failed to fetch tasks"}`);
        return;
      }

      renderTasks(allTasks); // Initial render with all tasks
    } catch (error) {
      console.error("Error fetching tasks:", error);
      alert("An error occurred while fetching tasks.");
    }
  };

  // Function to render tasks
  const renderTasks = (tasks) => {
    taskContainer.innerHTML = ""; // Clear task list

    tasks.forEach((task) => {
      const taskCard = document.createElement("div");
      taskCard.classList.add("task-item");
      const pointColor = getPointsColor(task.points);
      const status = task.points >= 100 ? "Done" : "In Progress";

      // Task content
      let taskContent = `
      <h3>${task.name}</h3>
      <p class="status"><strong>Status:</strong> ${status}</p>
      <p><strong>Points:</strong> 
        <span style="color: ${pointColor};">${task.points}</span>
      </p>
    `;

      // If an image is available, include it before the edit/delete buttons
      if (task.image_url && task.image_url.trim() !== "") {
        taskContent += `<div class="task-image-container">
        <img src="${task.image_url}" alt="Task Image" class="task-image"/>
      </div>`;
      }

      // Actions (Edit & Delete buttons)
      taskContent += `
      <div class="actions">
        <button class="cta secondary edit-task" data-id="${task.taskId}">Edit</button>
        <button class="cta secondary delete-task" data-id="${task.taskId}">Delete</button>
      </div>
    `;

      taskCard.innerHTML = taskContent;
      taskContainer.appendChild(taskCard);
    });

    attachEventListeners(); // Reattach event listeners
  };

  // Function to filter tasks based on search input
  const filterTasks = () => {
    const searchTerm = searchBar.value.toLowerCase();
    const filteredTasks = allTasks.filter((task) =>
      task.name.toLowerCase().includes(searchTerm)
    );

    renderTasks(filteredTasks);
  };

  // Attach event listener to the search bar
  if (searchBar) {
    searchBar.addEventListener("input", filterTasks);
  }

  // Function to delete a task
  const deleteTask = async (taskId) => {
    try {
      const token = localStorage.getItem("jwt_token");

      const response = await fetch(
        `http://127.0.0.1:5000/api/tasks/${taskId}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.ok) {
        alert("Task deleted successfully!");
        fetchTasks(); // Refresh task list
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.error || "Failed to delete task"}`);
      }
    } catch (error) {
      console.error("Error deleting task:", error);
      alert("An error occurred while deleting the task.");
    }
  };

  // Function to attach event listeners to edit & delete buttons
  const attachEventListeners = () => {
    document.querySelectorAll(".edit-task").forEach((button) => {
      button.addEventListener("click", (event) => {
        const taskId = event.target.getAttribute("data-id");
        if (taskId) {
          window.location.href = `/create_task?taskId=${taskId}`;
        }
      });
    });

    document.querySelectorAll(".delete-task").forEach((button) => {
      button.addEventListener("click", async (event) => {
        const taskId = event.target.getAttribute("data-id");
        await deleteTask(taskId);
      });
    });
  };

  // Fetch tasks on page load (Only if user is on tasks.html)
  if (window.location.pathname.includes("tasks")) {
    await fetchTasks();
  }
});
