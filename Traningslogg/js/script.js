// script.js

document.addEventListener("DOMContentLoaded", async function () {
  let exercises = [];

  try {
    const res = await fetch("/api/exercises");
    exercises = await res.json();
    if (!Array.isArray(exercises)) throw new Error("Invalid exercise data");
  } catch (err) {
    console.error("Kunde inte hämta övningar:", err);
    exercises = [];
  }

  const passwordInput = document.getElementById("myInput");
  const checkbox = document.getElementById("showPassword");
  if (checkbox && passwordInput) {
    checkbox.addEventListener("change", function () {
      passwordInput.type = this.checked ? "text" : "password";
    });
  }

  const registerForm = document.getElementById("registerForm");
  if (registerForm) {
    registerForm.addEventListener("submit", async function (event) {
      event.preventDefault();
      const email = document.getElementById("first").value;
      const username = document.getElementById("second").value;
      const password = passwordInput.value;

      try {
        const response = await fetch("/api/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, username, password })
        });

        const result = await response.json();
        if (response.ok) {
          alert("Registrering lyckades!");
          window.location.href = "login.html";
        } else {
          alert(result.error || "Något gick fel.");
        }
      } catch (error) {
        console.error("Fel vid registrering:", error);
        alert("Ett tekniskt fel uppstod.");
      }
    });
  }

  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", async function (event) {
      event.preventDefault();

      const email = document.getElementById("first").value;
      const password = passwordInput.value;

      try {
        const response = await fetch("/api/users");
        const users = await response.json();

        const user = users.find(u => u.email === email && u.password === password);
        if (user) {
          localStorage.setItem("loggedInUser", JSON.stringify(user));
          alert("Inloggning lyckades!");
          window.location.href = "../pages/profile.html";
        } else {
          alert("Fel e-post eller lösenord.");
        }
      } catch (error) {
        console.error("Fel vid inloggning:", error);
        alert("Ett tekniskt fel uppstod.");
      }
    });
  }

  const userEmailSpan = document.getElementById("userEmail");
  const userNameSpan = document.getElementById("userName");
  const storedUser = localStorage.getItem("loggedInUser");
  if (storedUser && userEmailSpan && userNameSpan) {
    const user = JSON.parse(storedUser);
    userEmailSpan.textContent = user.email;
    userNameSpan.textContent = user.username;
  }

  const logoutButton = document.getElementById("logoutButton");
  if (logoutButton) {
    logoutButton.addEventListener("click", function () {
      localStorage.removeItem("loggedInUser");
      window.location.href = "login.html";
    });
  }

  const metricBtn = document.getElementById("metricButton");
  const imperialBtn = document.getElementById("imperialButton");
  function setActiveUnit(unit) {
    if (metricBtn && imperialBtn) {
      metricBtn.classList.toggle("active", unit === "metric");
      imperialBtn.classList.toggle("active", unit === "imperial");
      localStorage.setItem("preferredUnit", unit);
    }
  }
  const savedUnit = localStorage.getItem("preferredUnit") || "metric";
  setActiveUnit(savedUnit);
  if (metricBtn && imperialBtn) {
    metricBtn.addEventListener("click", () => setActiveUnit("metric"));
    imperialBtn.addEventListener("click", () => setActiveUnit("imperial"));
  }

  let seconds = 0;
  const timerElement = document.getElementById("timer");
  function updateTimer() {
    seconds++;
    const hrs = String(Math.floor(seconds / 3600)).padStart(2, "0");
    const mins = String(Math.floor((seconds % 3600) / 60)).padStart(2, "0");
    const secs = String(seconds % 60).padStart(2, "0");
    if (timerElement) timerElement.textContent = `${hrs}:${mins}:${secs}`;
  }
  setInterval(updateTimer, 1000);

  const modal = document.getElementById("exerciseModal");
  const closeButton = document.querySelector(".close-button");
  const exerciseList = document.getElementById("exerciseList");
  const searchInput = document.getElementById("exerciseSearch");
  if (closeButton) closeButton.addEventListener("click", () => modal.classList.add("hidden"));
  if (searchInput) {
    searchInput.addEventListener("input", () => {
      renderExerciseList(searchInput.value);
    });
  }

  function renderExerciseList(filter) {
    if (!exerciseList || !Array.isArray(exercises)) return;
    exerciseList.innerHTML = "";
    const filtered = exercises.filter(ex =>
      ex.name.toLowerCase().includes(filter.toLowerCase())
    );
    filtered.forEach(exercise => {
      const li = document.createElement("li");
      li.textContent = exercise.name;
      li.addEventListener("click", () => {
        createExerciseElement(exercise);
        modal.classList.add("hidden");
      });
      exerciseList.appendChild(li);
    });
  }

  function createExerciseElement(exercise) {
    const workoutContainer = document.getElementById("workoutContainer");
    if (!workoutContainer) return;
    const div = document.createElement("div");
    div.className = "exercise";
    div.innerHTML = `
      <h3>${exercise.name}</h3>
      <p><strong>Utrustning:</strong> ${exercise.equipment}</p>
      <p><strong>Målmuskel:</strong> ${exercise.bodyPart}</p>
      <div class="set">
        <label>Set <span class="set-number">1</span></label>
        <label>Reps: <input type="number" value="0" /></label>
        <label>Weight (kg): <input type="number" value="0" /></label>
        <button class="delete-set">✖</button>
      </div>
      <button class="add-set">➕ Lägg till set</button>
      <button class="delete-exercise">🗑 Ta bort övning</button>
    `;
    workoutContainer.appendChild(div);

    div.querySelector(".add-set").addEventListener("click", function () {
      const newSet = document.createElement("div");
      newSet.className = "set";
      const setCount = div.querySelectorAll(".set").length + 1;
      newSet.innerHTML = `
        <label>Set <span class="set-number">${setCount}</span></label>
        <label>Reps: <input type="number" value="0" /></label>
        <label>Weight (kg): <input type="number" value="0" /></label>
        <button class="delete-set">✖</button>
      `;
      div.insertBefore(newSet, this);
      attachDeleteSetListener(newSet.querySelector(".delete-set"));
    });

    div.querySelector(".delete-exercise").addEventListener("click", () => div.remove());
    attachDeleteSetListener(div.querySelector(".delete-set"));
  }

  function attachDeleteSetListener(button) {
    if (button) {
      button.addEventListener("click", function () {
        const exerciseDiv = this.closest(".exercise");
        this.closest(".set").remove();
        updateSetNumbers(exerciseDiv);
      });
    }
  }

  function updateSetNumbers(exerciseDiv) {
    const sets = exerciseDiv.querySelectorAll(".set");
    sets.forEach((set, index) => {
      const numberSpan = set.querySelector(".set-number");
      if (numberSpan) numberSpan.textContent = index + 1;
    });
  }

  const addExerciseBtn = document.querySelector(".btn.blue");
  if (addExerciseBtn) {
    addExerciseBtn.addEventListener("click", function () {
      if (modal) modal.classList.remove("hidden");
      renderExerciseList("");
    });
  }

  const saveBtn = document.querySelector(".btn.green");
  if (saveBtn) {
    saveBtn.addEventListener("click", async function () {
      const workoutContainer = document.getElementById("workoutContainer");
      const exerciseDivs = workoutContainer.querySelectorAll(".exercise");
      const workout = {
        date: new Date().toDateString(),
        exercises: Array.from(exerciseDivs).map(div => {
          const name = div.querySelector("h3").textContent;
          const sets = div.querySelectorAll(".set").length;
          const reps = parseInt(div.querySelector(".set input[type='number']")?.value || 0);
          const weight = parseInt(div.querySelectorAll(".set input[type='number']")[1]?.value || 0);
          return { name, sets, reps, weight };
        })
      };

      const history = JSON.parse(localStorage.getItem("workoutHistory")) || [];
      history.unshift(workout);
      localStorage.setItem("workoutHistory", JSON.stringify(history));

      try {
        const response = await fetch("/api/save-workout", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(workout)
        });
        if (response.ok) {
          alert("Träningspass sparat!");
        } else {
          alert("Kunde inte spara till server.");
        }
      } catch (error) {
        console.error("Fel vid sparning:", error);
        alert("Tekniskt fel vid sparning.");
      }
    });
  }

  const container = document.getElementById("history-container");
  if (container) {
    const history = JSON.parse(localStorage.getItem("workoutHistory")) || [];
    function renderHistory() {
      container.innerHTML = "";
      history.forEach((workout, index) => {
        const div = document.createElement("div");
        div.className = "workout-entry";
        div.innerHTML = `
          <button class="delete-btn" data-index="${index}">X</button>
          <h2>Workout</h2>
          <p><strong>Status:</strong> Finished | ${workout.date || "Unknown Date"}</p>
          <p><strong>Exercises:</strong></p>
          <ul>
            ${workout.exercises.map(ex => `
              <li><strong>${ex.name}</strong><br>${ex.sets || 0} sets × ${ex.reps || 0} reps × ${ex.weight || 0} kg</li>
            `).join("")}
          </ul>
        `;
        container.appendChild(div);
      });
    }

    container.addEventListener("click", e => {
      if (e.target.classList.contains("delete-btn")) {
        const index = parseInt(e.target.dataset.index);
        history.splice(index, 1);
        localStorage.setItem("workoutHistory", JSON.stringify(history));
        renderHistory();
      }
    });

    renderHistory();
  }

  const historyContainer = document.getElementById("history-container");

  if (historyContainer) {
    try {
      // Hämta historik från servern
      const response = await fetch("/data/history.json");
      const history = await response.json();

      // Rendera historiken
      renderHistory(history);
    } catch (error) {
      console.error("Kunde inte hämta historik:", error);
      historyContainer.innerHTML = "<p>Det gick inte att ladda historiken.</p>";
    }
  }

  function renderHistory(history) {
    historyContainer.innerHTML = ""; // Rensa tidigare innehåll
    history.forEach((workout, index) => {
      const workoutDiv = document.createElement("div");
      workoutDiv.className = "workout-entry";
      workoutDiv.innerHTML = `
        <h2>Workout ${index + 1}</h2>
        <p><strong>Date:</strong> ${workout.date}</p>
        <ul>
          ${workout.exercises
            .map(
              (exercise) => `
            <li>
              <strong>${exercise.name}</strong>: ${exercise.sets} sets × ${exercise.reps} reps × ${exercise.weight} kg
            </li>
          `
            )
            .join("")}
        </ul>
      `;
      historyContainer.appendChild(workoutDiv);
    });
  }
});
