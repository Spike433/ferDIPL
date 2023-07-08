#include "DHT.h"
#include <ArduinoJson.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <WiFi.h>
#include <WiFiMulti.h>
#include <NTPClient.h>
#include <PubSubClient.h>

#include "mqtt_client.h"
#include "nvs_flash.h"

#define LED 3
#define DHTPIN 5
#define DHTTYPE DHT11

#define DHT11_TEMP (0)
#define DHT11_HUM (1)

// Initialize DHT sensor.
DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "";
const char* password = "";

const char* http_username = "";
const char* http_password = "";

char* mqttServer = "161.53.19.19";
int mqttPort = 56883;

const char* topic = "json/grupa23";    // define topic
const char* mqtt_username = "emqx";    // username for authentication
const char* mqtt_password = "public";  // password for authentication

WiFiServer my_server(80);
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");
WiFiClient client;


const esp_mqtt_client_config_t mqtt_cfg = {
  .uri = "ws://161.53.19.19:56183",
};

esp_mqtt_client_handle_t mqtt_client = esp_mqtt_client_init(&mqtt_cfg);

const char* test_root_ca =
  "-----BEGIN CERTIFICATE-----\n"
  "MIICljCCAX4CCQDuNMxqwX8x0zANBgkqhkiG9w0BAQsFADANMQswCQYDVQQGEwJI\n"
  "UjAeFw0yMzA0MDcxMTExMzRaFw0yNDA0MDYxMTExMzRaMA0xCzAJBgNVBAYTAkhS\n"
  "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4GzpRFVtN14J/AVOOu8M\n"
  "e/DvsthWiuFHv4wVAqA0XJN36w9K2DSI50CBg5zQexX8DJGRBBMzOPjlvNlBMW0N\n"
  "VAkSrB/p61puKHInJJO+zjKI7lNpMvW6ca06jVWYabtYEf81c/xdCYad8BO6Zw3Q\n"
  "BgslYifTbO2H97wZyZrVhSlNcp4rjviJx6D68aeVEdd6EMuyYhL0wUZ5g5Btz05y\n"
  "HLpTKshSTtkNzN3Hsw/XBE/+6TbW8+PDBjyx1hLW7aOZZEk6x+CiEH2vUnKSAcLY\n"
  "dBmHiwzk5vckWL28yFw/b0VDdfhaDRosbxlTYWYq/HB6lBCXS+s8S9lnzcv9mwIj\n"
  "jwIDAQABMA0GCSqGSIb3DQEBCwUAA4IBAQDSNuA1VZn0c8ylxkQ0yl+obppeJu2x\n"
  "oXpRF7jFCW0GOoRyYF/lrm3Ecb1ur/DARsBdUaO1urVJiFI6Dl4hSObrXJzn5Le0\n"
  "MMi6lJNb/3gJxTn1MTLDS1w7S1IQGLsKQ9AsSjR7BYxfyDshOpW53FBNqu1uuJTA\n"
  "RPd8upnMZ5jULMJm/BTL2ZaW+/o8JiVtj+/Ed0Tty0zGJUfqtNKnltzNPOFsNbz/\n"
  "BvpHhNW/F1Rh+iortqzqfSUNWOTlHKogtswBC5Stw9uqiBO6nq9tOc27Zey6SHlF\n"
  "fLpy1fTqT/3+UX1y3lQabKqbdqeo/tk7wAA44pzbcmvvqiPI44Z8RUzL\n"
  "-----END CERTIFICATE-----\n";



String decodeJson(float data, unsigned long tmsp, int option) {
  StaticJsonBuffer<200> jsonBuffer;

  JsonObject& root = jsonBuffer.createObject();
  root["deviceId"] = "Grupa23DeviceHum";

  JsonObject& header = root.createNestedObject("header");
  header["timestamp"] = String(tmsp);

  JsonObject& body = root.createNestedObject("body");
  if (option == DHT11_TEMP) {
    JsonObject& dht_temp = body.createNestedObject("G23DHT");
    dht_temp["G23Temp"] = String(data);
  } else {
    JsonObject& dht_hum = body.createNestedObject("G23DHT");
    dht_hum["G23Hum"] = String(data);
  }
  String jsonString;
  root.printTo(jsonString);

  //root.printTo(Serial);

  return jsonString;
}


// Variable to save current epoch time
unsigned long epochTime;

unsigned long getTime() {
  timeClient.setTimeOffset(3600 * 2);
  timeClient.update();
  unsigned long now = timeClient.getEpochTime();
  return now;
}

int read_dht11(void) {
  // Wait a few seconds between measurements.
  delay(3000);

  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return -1;
  }

  // Compute heat index in Celsius (isFahreheit = false)
 // float hic = dht.computeHeatIndex(t, h, false);

  /*Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.println(F("°C "));*/
  
  /*
  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("°F  Heat index: "));
  Serial.print(hic);
  */

  return t;
}

void connect_to_wifi(void) {
  Serial.print("Attempting to connect to SSID: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  // attempt to connect to Wifi network:
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    // wait 1 second for re-trying
    delay(1000);
  }

  Serial.print("Connected to ");
  Serial.println(ssid);

  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  //  client.setCACert(test_root_ca);
  //client.setInsecure();
}

void send_http_request(float data) {
  HTTPClient http;
  String URL = "https://161.53.19.19:56443/m2m/data";

  http.begin(URL);  // Works with HTTP

  http.addHeader("Content-Type", "application/vnd.ericsson.simple.input.hierarchical+json;version=1.0");
  http.setAuthorization(http_username, http_password);

  // String httpRequestData = "{\"deviceId\" : \"Grupa23DeviceHum\",\"header\":{\"timestamp\" : 1685038903},\"body\":{\"G23DHT\":{\"G23Temp\":73.33}}}";
  String httpRequestData = decodeJson(data, timeClient.getEpochTime(), DHT11_TEMP);
  Serial.println(httpRequestData);

  int httpCode = http.POST(httpRequestData);

  Serial.print("HTTP Response code: ");
  Serial.println(httpCode);

  http.end();
}

static void mqtt_event_handler(void* handler_args, esp_event_base_t base, int32_t event_id, void* event_data) {
  ESP_LOGD(TAG, "Event dispatched from event loop base=%s, event_id=%d", base, event_id);
  esp_mqtt_event_handle_t event = (esp_mqtt_event_handle_t)event_data;
  int msg_id;
  switch ((esp_mqtt_event_id_t)event_id) {
    case MQTT_EVENT_CONNECTED:
      ESP_LOGI(TAG, "MQTT_EVENT_CONNECTED");

      msg_id = esp_mqtt_client_subscribe(mqtt_client, "grupa23", 0);
      ESP_LOGI(TAG, "sent subscribe successful, msg_id=%d", msg_id);
      msg_id = esp_mqtt_client_publish(mqtt_client, "grupa23", "data_3", 0, 1, 0);
      ESP_LOGI(TAG, "sent publish successful, msg_id=%d", msg_id);

      //msg_id = esp_mqtt_client_unsubscribe(mqtt_client, "/topic/qos1");
      break;
    case MQTT_EVENT_DISCONNECTED:
      ESP_LOGI(TAG, "MQTT_EVENT_DISCONNECTED");
      break;

    case MQTT_EVENT_SUBSCRIBED:
      ESP_LOGI(TAG, "MQTT_EVENT_SUBSCRIBED, msg_id=%d", event->msg_id);
      // msg_id = esp_mqtt_client_publish(client, "/topic/qos0", "data", 0, 0, 0);
      // ESP_LOGI(TAG, "sent publish successful, msg_id=%d", msg_id);
      break;
    case MQTT_EVENT_UNSUBSCRIBED:
      ESP_LOGI(TAG, "MQTT_EVENT_UNSUBSCRIBED, msg_id=%d", event->msg_id);
      break;
    case MQTT_EVENT_PUBLISHED:
      ESP_LOGI(TAG, "MQTT_EVENT_PUBLISHED, msg_id=%d", event->msg_id);
      break;
    case MQTT_EVENT_DATA:
      ESP_LOGI(TAG, "MQTT_EVENT_DATA");
      printf("TOPIC=%.*s\r\n", event->topic_len, event->topic);
      printf("DATA=%.*s\r\n", event->data_len, event->data);

      if(event->data_len == 7)
      {
        digitalWrite(LED, HIGH); 
      }
      else
      {
        digitalWrite(LED, LOW); 
      }
      break;
    case MQTT_EVENT_ERROR:
      ESP_LOGI(TAG, "MQTT_EVENT_ERROR");
      break;
    default:
      ESP_LOGI(TAG, "Other event id:%d", event->event_id);
      break;
  }
}


static void mqtt_app_start(void) {

  // The last argument may be used to pass data to the event handler, in this example mqtt_event_handler
  esp_mqtt_client_register_event(mqtt_client, (esp_mqtt_event_id_t)ESP_EVENT_ANY_ID, mqtt_event_handler, NULL);
  esp_mqtt_client_start(mqtt_client);
}


void setup() {
  pinMode(LED, OUTPUT);

  Serial.begin(9600);
  Serial.println(F("DHTxx test!"));

  dht.begin();
  connect_to_wifi();
  timeClient.begin();

  nvs_flash_init();
  esp_netif_init();

  mqtt_app_start();
}

void loop() {
  float temp = read_dht11();

  // publish and subscribe
  send_http_request(temp);

  esp_mqtt_client_publish(mqtt_client, "grupa23", "enabled", 0, 1, 0);
}

