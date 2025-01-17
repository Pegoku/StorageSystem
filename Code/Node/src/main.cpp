#include <Arduino.h>
#include <Adafruit_NeoPixel.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <WebServer.h>

#include <.env>

Adafruit_NeoPixel strip = Adafruit_NeoPixel(positions, 15, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel slotLed = Adafruit_NeoPixel(16, 4, NEO_GRB + NEO_KHZ800);
WebServer server(4444);

const size_t capacity = JSON_OBJECT_SIZE(10) + 200;
StaticJsonDocument<capacity> jsonDocument;

char buffer[1024];

void locate(int position, JsonArray slotArray)
{
    position = position - 1;

    if (position < 0 || position >= positions)
    {
        Serial.println("Invalid position");
        server.send(400, "text/plain", "Invalid position");
        return;
    }
    else
    {
        server.send(200, "application/json", "{\"success\": true}");

        Serial.println("Locating position " + String(position));
        strip.clear();
        strip.setPixelColor(position, strip.Color(5, 5, 5));
        strip.show();
        String slotArrayStr;
        serializeJson(slotArray, slotArrayStr);
        Serial.println("Locating slots " + slotArrayStr);
        for (size_t i = 0; i < slotArray.size(); i++)
        {
            slotLed.setPixelColor(slotArray[i].as<int>() - 1, slotLed.Color(5, 5, 5));
        }
        slotLed.show();

        delay(5505);
        strip.clear();
        strip.show();
        slotLed.clear();
        slotLed.show();
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
    Serial.println(payload);

    int position = jsonDocument["position"];
    JsonArray slotJsonArray = jsonDocument["slot"].as<JsonArray>();
    int slotArray[slotJsonArray.size()];
    for (size_t i = 0; i < slotJsonArray.size(); i++)
    {
        slotArray[i] = slotJsonArray[i];
    }

    Serial.println(jsonDocument["position"].as<int>());
    for (size_t i = 0; i < slotJsonArray.size(); i++)
    {
        Serial.println(slotArray[i]);
    }

    locate(position, slotJsonArray);
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

    String nodeInfo = "{\"id\": " + String(node) + ", \"ip\": \"" + WiFi.localIP().toString() + "\", \"positions\": " + String(positions) + "}";
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
                    Serial.println("Check logs. Possible error in adding node");
                    // while (true)
                    // {
                    //     Serial.println(payload);
                    //     strip.fill(strip.Color(255, 0, 0), 0, positions);
                    //     strip.show();
                    //     delay(500);
                    //     strip.fill(strip.Color(0, 0, 0), 0, positions);
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
