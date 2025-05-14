// server.js

const express = require("express");
const fs = require("fs");
const path = require("path");
const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Server static files (HTML, CSS, JS, IMG)
app.use(express.static(__dirname));

// Sökvägar till JSON-filer
const usersPath = path.join(__dirname, "data", "users.json");
const exercisesPath = path.join(__dirname, "data", "exercises.json");

// === ANVÄNDARE ===
// Hämta alla användare
app.get("/api/users", (req, res) => {
    fs.readFile(usersPath, "utf8", (err, data) => {
        if (err) {
            console.error("Fel vid läsning av users.json:", err);
            return res.status(500).json({ error: "Kunde inte läsa filen." });
        }
        res.json(JSON.parse(data));
    });
});

// Registrera ny användare
app.post("/api/register", (req, res) => {
    const { email, username, password } = req.body;

    fs.readFile(usersPath, "utf8", (err, data) => {
        if (err) {
            console.error("Fel vid läsning av users.json:", err);
            return res.status(500).json({ error: "Kunde inte läsa filen." });
        }

        const users = JSON.parse(data);

        const existingUser = users.find(user => user.email === email);
        if (existingUser) {
            return res.status(400).json({ error: "Användaren finns redan!" });
        }

        const newUser = { email, username, password };
        users.push(newUser);

        fs.writeFile(usersPath, JSON.stringify(users, null, 2), (err) => {
            if (err) {
                console.error("Fel vid skrivning till users.json:", err);
                return res.status(500).json({ error: "Kunde inte spara användaren." });
            }
            res.status(201).json({ message: "Registreringen lyckades!" });
        });
    });
});

// === ÖVNINGAR ===
// Hämta alla övningar
app.get("/api/exercises", (req, res) => {
    fs.readFile(exercisesPath, "utf8", (err, data) => {
        if (err) {
            console.error("Fel vid läsning av exercises.json:", err);
            return res.status(500).json({ error: "Kunde inte läsa övningar." });
        }
        res.json(JSON.parse(data));
    });
});

// Lägg till en ny övning
app.post("/api/exercises", (req, res) => {
    const newExercise = req.body;

    fs.readFile(exercisesPath, "utf8", (err, data) => {
        if (err) {
            console.error("Fel vid läsning av exercises.json:", err);
            return res.status(500).json({ error: "Kunde inte läsa övningar." });
        }

        const exercises = JSON.parse(data);
        exercises.push(newExercise);

        fs.writeFile(exercisesPath, JSON.stringify(exercises, null, 2), (err) => {
            if (err) {
                console.error("Fel vid skrivning till exercises.json:", err);
                return res.status(500).json({ error: "Kunde inte spara övning." });
            }
            res.status(201).json({ message: "Övning sparad!" });
        });
    });
});

// === SPARA TRÄNINGSPASS ===
const historyPath = path.join(__dirname, "data", "history.json");

app.post("/api/save-workout", (req, res) => {
    const newWorkout = req.body;

    fs.readFile(historyPath, "utf8", (err, data) => {
        let history = [];
        if (!err && data) {
            try {
                history = JSON.parse(data);
            } catch (parseErr) {
                console.error("Kunde inte parsa history.json:", parseErr);
            }
        }

        history.unshift(newWorkout); // senaste först

        fs.writeFile(historyPath, JSON.stringify(history, null, 2), (err) => {
            if (err) {
                console.error("Fel vid sparning av träningspass:", err);
                return res.status(500).json({ error: "Kunde inte spara träningspass." });
            }
            res.status(201).json({ message: "Träningspass sparat!" });
        });
    });
});

// Starta servern
app.listen(PORT, () => {
    console.log(`🚀 Servern körs på http://localhost:${PORT}`);
});
