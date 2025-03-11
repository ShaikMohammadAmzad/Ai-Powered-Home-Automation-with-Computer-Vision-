# **Human Presence Detection and Automation System**  

## **Objective**  
This project aims to develop an automated human presence detection system using Python-based image processing. The system detects human presence in a room and wirelessly communicates with an ESP32 microcontroller via Wi-Fi. The ESP32 then controls electrical appliances like LEDs and a DC motor through a relay module, optimizing energy management and automation.  

## **System Overview**  
1. **Image Processing**:  
   - A camera captures images at regular intervals.  
   - Python-based image processing compares the captured image with reference images to detect human presence.  

2. **Wireless Communication**:  
   - Upon detection, the system sends a signal to the ESP32 microcontroller using the Wi-Fi protocol.  

3. **Appliance Control**:  
   - The ESP32 triggers a relay module to control electrical appliances.  
   - If a human is detected, the lights turn on; otherwise, they remain off.  

## **Features**  
- **Automated Energy Management**: Prevents unnecessary power consumption.  
- **Wireless Operation**: Eliminates the need for wired connections.  
- **Scalability**: Can integrate with multiple devices for a smart home setup.  

## **Technologies Used**  
- **Python** (OpenCV for image processing)  
- **ESP32** (Wi-Fi-enabled microcontroller)  
- **Relay Module** (For appliance control)  

## **Conclusion**  
This system ensures efficient energy management by automating appliance control based on human presence detection, contributing to smart home automation and energy conservation.
