# 🌿 Smart Air Quality Monitoring System using IoT & Fuzzy Logic AI

---

## 📌 Project Overview

The Smart Air Quality Monitoring System is an intelligent IoT-based project developed using Arduino Nano, MQ135 Gas Sensor, Python Dashboard, and Fuzzy Logic AI.
The system continuously monitors air quality, visualizes live sensor data, predicts air quality conditions using fuzzy logic, and provides real-time safety recommendations.

---

## ✨ Features

- Real-time air quality monitoring
- Live dashboard visualization
- Dual-line graph representation
- Fuzzy Logic AI implementation
- Intelligent safety recommendations
- Buzzer hardware alerts
- Real-time serial communication
- Stable AQI prediction using averaged values

---

## 🧠 AI Implementation

This project uses Fuzzy Logic AI to intelligently interpret MQ135 sensor readings instead of relying only on fixed thresholds.

### Why Fuzzy Logic?

Raw MQ135 sensor values fluctuate frequently due to environmental conditions.

Fuzzy logic helps to:

- Reduce sensor noise
- Smooth fluctuations
- Predict meaningful AQI values
- Generate intelligent safety measures
- Improve reliability

---

## 🛠️ Technologies Used

### Hardware Components

- Arduino Nano
- MQ135 Gas Sensor
- Buzzer
- Breadboard
- Jumper Wires

### Software & Libraries

- Python
- Arduino IDE
- Dash
- Plotly
- PySerial
- NumPy
- Scikit-Fuzzy
- SciPy

---

## 📊 Dashboard Features

### 📈 Real-Time Monitoring

- Displays live MQ135 sensor readings
- Updates dashboard continuously

### 📉 Dual-Line Graph

#### 🔴 Raw MQ135 Values
Shows direct sensor values from MQ135.

#### 🔵 Fuzzy AQI Values
Shows AI-processed air quality values.

### 🛡️ Safety Measures

The dashboard intelligently recommends:

- Wear a mask
- Avoid outdoor activities
- Improve indoor ventilation
- Use air purifier

---

## 📂 Project Structure

```
Smart-Air-Quality-Monitoring-System/
│
├── app.py
├── fuzzy_aqi.py
├── sketch_apr9c.ino
├── requirements.txt
├── README.md
│
└── assets/
    └── dashboard.png
```

---

---


## 📈 Working Principle

1. MQ135 sensor detects gases and pollutants.
2. Arduino reads analog values.
3. Sensor values are sent to Python using serial communication.
4. Dashboard receives real-time data.
5. Fuzzy Logic AI processes sensor readings.
6. AQI condition is predicted.
7. Safety measures are displayed.
8. Buzzer provide hardware alerts.

---

## 🔮 Future Enhancements

- Cloud Integration
- Mobile App Support
- SMS/Email Alerts
- Machine Learning Prediction
- IoT Remote Monitoring
- Data Logging & Analytics
- Smart Home Integration

---

## 🎓 Academic Relevance

This project demonstrates concepts of:

- Internet of Things (IoT)
- Artificial Intelligence
- Fuzzy Logic Systems
- Embedded Systems
- Data Visualization
- Real-Time Monitoring

---

## 👨‍💻 Author

### Nandeesh M N

