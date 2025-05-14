const exercises = [
  {
    name: "Bench Press",
    equipment: "Barbell",
    bodyPart: "Chest"
  },
  {
    name: "Squat",
    equipment: "Barbell",
    bodyPart: "Legs"
  },
  {
    name: "Deadlift",
    equipment: "Barbell",
    bodyPart: "Back"
  },
  {
    name: "Pull-Up",
    equipment: "Bodyweight",
    bodyPart: "Back"
  },
  {
    name: "Push-Up",
    equipment: "Bodyweight",
    bodyPart: "Chest"
  },
  {
    name: "Bicep Curl",
    equipment: "Dumbbell",
    bodyPart: "Arms"
  },
  {
    name: "Tricep Dip",
    equipment: "Bodyweight",
    bodyPart: "Arms"
  },
  {
    name: "Lunges",
    equipment: "Bodyweight",
    bodyPart: "Legs"
  },
  {
    name: "Plank",
    equipment: "Bodyweight",
    bodyPart: "Core"
  },
  {
    name: "Shoulder Press",
    equipment: "Dumbbell",
    bodyPart: "Shoulders"
  },
  {
    name: "Leg Press",
    equipment: "Machine",
    bodyPart: "Legs"
  },
  {
    name: "Lat Pulldown",
    equipment: "Machine",
    bodyPart: "Back"
  },
  {
    name: "Chest Fly",
    equipment: "Machine",
    bodyPart: "Chest"
  },
  {
    name: "Calf Raise",
    equipment: "Bodyweight",
    bodyPart: "Legs"
  },
  {
    name: "Russian Twist",
    equipment: "Bodyweight",
    bodyPart: "Core"
  }
];

const listContainer = document.getElementById("exercise-list");
const searchInput = document.getElementById("search");

const render = (items) => {
  listContainer.innerHTML = "";
  items.forEach(ex => {
    const li = document.createElement("li");
    li.innerHTML = `<strong>${ex.name} (${ex.equipment})</strong><br>${ex.bodyPart}`;
    listContainer.appendChild(li);
  });
};

render(exercises);

searchInput.addEventListener("input", (e) => {
  const value = e.target.value.toLowerCase();
  const filtered = exercises.filter(ex => ex.name.toLowerCase().includes(value));
  render(filtered);
});

module.exports = exercises;
