# Anti-Sleep Glasses

This project detects closed eyes using OpenCV and triggers an alert via an ESP32. If eyes stay closed for more than 10 seconds, an LED or buzzer connected to GPIO12 flickers. When eyes open, the alert stops.

- Face and eye detection using Haar cascades
- 10-second eye-closure timer
- Serial communication to ESP32
- Flickering LED/buzzer alert

![image](https://github.com/user-attachments/assets/b1fa6989-482c-4cec-824c-17d28f9b2b8a)
