// Smooth Scrolling for Navigation Links
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
