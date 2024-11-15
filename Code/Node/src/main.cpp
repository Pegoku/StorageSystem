#include <Arduino.h>
#include <Adafruit_NeoPixel.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <WebServer.h>

#include <.env>

Adafruit_NeoPixel strip = Adafruit_NeoPixel(slots, 15, NEO_GRB + NEO_KHZ800);

WebServer server(4444);

JsonDocument jsonDocument;
char buffer[1024];

void locate(int slot)
{
    slot = slot - 1;

    if (slot < 0 || slot >= slots)
    {
        Serial.println("Invalid slot");
        server.send(400, "text/plain", "Invalid slot");
        return;
    }
    else
    {
        server.send(200, "application/json", "{\"success\": true}");

        Serial.println("Locating slot " + String(slot));
        strip.clear();
        strip.setPixelColor(slot, strip.Color(5, 5, 5));
        strip.show();
        delay(5000);
        strip.clear();
        strip.show();

    }
}

void handlePost()
{
    Serial.println("POST request received");
    if (server.hasArg("plain") == false)
    {
        server.send(400, "text/plain", "Payload not found");
        return;
    }

    Serial.println("Payload found");
    String payload = server.arg("plain");
    deserializeJson(jsonDocument, payload);
    Serial.println("Deserialized JSON");

    int slot = jsonDocument["slot"];
    locate(slot);
}

void setupServer()
{
    Serial.println("Setting up server");
    server.on("/locate", HTTP_POST, handlePost);
    server.begin();
    Serial.println("Server started");
}

void setup()
{
    Serial.begin(115200);
    delay(1000);
    Serial.println("Hello World");

    strip.begin();

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }

    Serial.println("Connected to WiFi");

    Serial.println(WiFi.localIP());
    delay(1000);

    String nodeInfo = "{\"id\": " + String(node) + ", \"ip\": \"" + WiFi.localIP().toString() + "\", \"slots\": " + String(slots) + "}";
    if (WiFi.status() == WL_CONNECTED)
    {
        HTTPClient http;
        http.begin("http://" + String(server_IP) + ":" + String(server_port) + "/api/addnode");
        http.addHeader("Content-Type", "application/json");
        int httpCode = http.POST(nodeInfo);
        if (httpCode > 0)
        {
            String payload = http.getString();
            Serial.println(payload);
            http.end();

            JsonDocument doc;
            DeserializationError error = deserializeJson(doc, payload);

            if (!error)
            {
                bool success = doc["success"];
                if (success)
                {
                    Serial.println("Node added successfully");
                }
                else
                {
                    Serial.println("Failed to add node");
                    // while (true)
                    // {
                    //     Serial.println(payload);
                    //     strip.fill(strip.Color(255, 0, 0), 0, slots);
                    //     strip.show();
                    //     delay(500);
                    //     strip.fill(strip.Color(0, 0, 0), 0, slots);
                    //     strip.show();
                    //     delay(500);
                    // }
                }
            }
            else
            {
                Serial.println("Failed to parse JSON response");
            }
        }
        else
        {
            Serial.println("HTTP request failed");
        }
    }
    else
    {
        Serial.println("WiFi not connected");
    }

    setupServer();
}

void loop()
{
    server.handleClient();
}
