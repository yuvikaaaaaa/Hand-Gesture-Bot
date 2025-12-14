# Vision-Based Hand Gesture Controlled Robot using OpenCV

## 📌 Project Overview
This project implements a **vision-based hand gesture controlled robot (software simulation)** using **OpenCV and MediaPipe**.  
The system uses real-time hand gestures captured through a camera to control the **direction and speed** of a virtual robot.  
It demonstrates **human–robot interaction**, **closed-loop control**, and **gesture-based automation**.

---

## 🎯 Objectives
- To design a contactless robot control system using computer vision
- To recognize hand gestures in real time
- To implement bimanual gesture control (direction + speed)
- To improve robustness using temporal filtering
- To simulate robot motion within a bounded workspace

---

## 🛠️ Technologies Used
- Python  
- OpenCV  
- MediaPipe  
- NumPy  
- Visual Studio Code  

---

## ⚙️ System Description

### 🔹 Gesture Control Logic
- **Right Hand** → Controls robot direction  
- **Left Hand** → Controls robot speed  

### 🔹 Gesture Mapping (Right Hand)

| Fingers | Command |
|--------|--------|
| 0 | STOP |
| 1 | FORWARD |
| 2 | LEFT |
| 3 | RIGHT |
| 4 | BACKWARD |

### 🔹 Speed Control (Left Hand)
- Speed = Number of fingers × constant factor

---

## 🔁 Robust Gesture Recognition
To reduce noise and gesture flickering, **temporal filtering** is implemented.  
The system stores the last five detected commands and applies **majority voting** to obtain a stable final command.

---

## 🤖 Robot Simulation
- The robot is represented as a virtual object on the screen
- Moves based on stabilized gesture commands
- Boundary conditions prevent the robot from leaving the visible workspace

---

## ▶️ How to Run the Project
1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

Note: finger_count.py is the main implementation file of the project.
Other files were used during development and testing.
