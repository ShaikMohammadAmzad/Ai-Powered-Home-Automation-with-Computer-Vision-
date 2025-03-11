#include <WiFi.h>
#include <WebServer.h>  // ESP32 specific WebServer library

// WiFi credentials
const char* ssid = "POCO X6 Pro 5G";   // Enter your WiFi SSID
const char* password = "0000000000";   // Enter your WiFi Password

WebServer server(80); // HTTP Server on port 80

#define LED_PIN 5       // GPIO5 (D5) for LED
#define MOTOR_PIN 12     // GPIO4 (D4) for DC Motor

void controlDevice() {
    if (server.hasArg("state")) { 
        int state = server.arg("state").toInt(); 

        if (state == 1) {
            digitalWrite(LED_PIN, HIGH);
            digitalWrite(MOTOR_PIN, LOW);
            Serial.println("LED and Motor turned ON");
            server.send(200, "text/plain", "LED and Motor ON");
        } 
        else if (state == 0) {
            digitalWrite(LED_PIN, LOW);
            digitalWrite(MOTOR_PIN, HIGH);
            Serial.println("LED and Motor turned OFF");
            server.send(200, "text/plain", "LED and Motor OFF");
        } 
        else {
            server.send(400, "text/plain", "Invalid State. Use 1 or 0.");
        }
    } 
    else {
        server.send(400, "text/plain", "Missing state parameter.");
    }
}

void setup() {
    Serial.begin(115200);
    Serial.println("\nInitializing...");

    pinMode(LED_PIN, OUTPUT);
    pinMode(MOTOR_PIN, OUTPUT);

    // Ensure both start OFF
    digitalWrite(LED_PIN, LOW);
    digitalWrite(MOTOR_PIN, HIGH);

    Serial.print("Connecting to WiFi");
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWiFi Connected!");
    Serial.println("ESP32 IP Address: " + WiFi.localIP().toString());

    server.on("/control", controlDevice); // Example: /control?state=1
    server.begin();
}

void loop() {
    server.handleClient();
}
