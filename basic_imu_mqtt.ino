#include <WiFi.h>
#include <PubSubClient.h>
//#include "arduino_secrets.h"
//#define SECRET_SSID "UCLA_WIFI"
//#define SECRET_SSID "Yubin's Chinese Dry Cleaning"
//#define SECRET_PASS "Bruins4Recovery, LLC"
//#define SECRET_SSID "UCLA_WIFI"
//#define SECRET_PASS ""
#define SECRET_SSID "Keaton"
#define SECRET_PASS ""  // insert password here
#include "ICM_20948.h" // Click here to get the library: http://librarymanager/All#SparkFun_ICM_20948_IMU

#include <iostream>

// for circular motion classifier:
#include <vector>
#include <cmath>
std::vector<unsigned long> timestamps_Y;
std::vector<unsigned long> timestamps_Z;

//#define USE_SPI       // Uncomment this to use SPI

#define SERIAL_PORT Serial

#define SPI_PORT SPI // Your desired SPI port.       Used only when "USE_SPI" is defined
#define CS_PIN 2     // Which pin you connect CS to. Used only when "USE_SPI" is defined

#define WIRE_PORT Wire // Your desired Wire port.      Used when "USE_SPI" is not defined
// The value of the last bit of the I2C address.
// On the SparkFun 9DoF IMU breakout the default is 1, and when the ADR jumper is closed the value becomes 0
#define AD0_VAL 1

#ifdef USE_SPI
ICM_20948_SPI myICM; // If using SPI create an ICM_20948_SPI object
#else
ICM_20948_I2C myICM; // Otherwise create an ICM_20948_I2C object
#endif

// WiFi
const char *ssid = SECRET_SSID; // Enter your WiFi name
const char *password = SECRET_PASS;  // Enter WiFi password

// MQTT Broker
// const char *mqtt_broker = "broker.emqx.io";
// const char *topic = "ece180d/test";
// const char *mqtt_username = "emqx";
// const char *mqtt_password = "public";
// const int mqtt_port = 1883;

// MQTT Broker
const char *mqtt_broker = "mqtt.eclipseprojects.io";
const char *topic = "esp32/testKeaton";
// const char *mqtt_username = "emqx";
// const char *mqtt_password = "public";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
 // Set software serial baud to 115200;
 Serial.begin(115200);
 // connecting to a WiFi network
 WiFi.begin(ssid, password);
 while (WiFi.status() != WL_CONNECTED) {
     delay(500);
     Serial.println("Connecting to WiFi..");
 }
 Serial.println("Connected to the WiFi network");
 //connecting to a mqtt broker
 client.setServer(mqtt_broker, mqtt_port);
 client.setCallback(callback);
 while (!client.connected()) {
     String client_id = "esp32-client-";
     client_id += String(WiFi.macAddress());
     Serial.printf("The client %s connects to the public mqtt broker\n", client_id.c_str());
     if (client.connect(client_id.c_str())) { //, mqtt_username, mqtt_password)) {
         Serial.println("mqtt broker connected");
     } else {
         Serial.print("failed with state ");
         Serial.print(client.state());
         delay(2000);
     }
 }
 // publish and subscribe
 client.publish(topic, "Hi I'm ESP32 ^^");
 client.subscribe(topic);

  #ifdef USE_SPI
    SPI_PORT.begin();
  #else
    WIRE_PORT.begin();
    WIRE_PORT.setClock(400000);
  #endif

  bool initialized = false;
  while (!initialized) {
    #ifdef USE_SPI
      myICM.begin(CS_PIN, SPI_PORT);
    #else
      myICM.begin(WIRE_PORT, AD0_VAL);
    #endif

    SERIAL_PORT.print(F("Initialization of the sensor returned: "));
    SERIAL_PORT.println(myICM.statusString());
    if (myICM.status != ICM_20948_Stat_Ok) {
      SERIAL_PORT.println("Trying again...");
      delay(500);
    } else {
      initialized = true;
    }
  }
}

void callback(char *topic, byte *payload, unsigned int length) {
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char) payload[i]);
  }
  Serial.println();
  Serial.println("-----------------------");
}

void loop()
{

  //SERIAL_PORT.print("looping...");
  //client.publish("esp32/testKeaton","Looping...");
  if (myICM.dataReady())
  {
    myICM.getAGMT();         // The values are only updated when you call 'getAGMT'
                             //    printRawAGMT( myICM.agmt );     // Uncomment this to see the raw values, taken directly from the agmt structure
    // Push forward, no action and upward motion classifier:
    //SERIAL_PORT.print("Publishing...");
    float stabThreshold = 1200;
    float swipeUpThreshold = 1200;
    float swipeLeftThreshold = 1200;
    float scaled_accZ = myICM.accZ() - 980;
    float idleThreshold = 400;

    // stabbing motion classifier
    // if the x acceleration is above a threshold and it's not due to gravity (i.e. tilt)
    if (myICM.accX() > stabThreshold && (myICM.accZ() + myICM.accY()) > (980 - 200)) {
      client.publish("esp32/testKeaton","Stabbing motion.");
    }
    // swipe up classifier
    // we should also technically check that the IMU is not upside down
    if (scaled_accZ > swipeUpThreshold) {
      client.publish("esp32/testKeaton","Swipe Up.");
    }

    // swipe left
    if (myICM.accY() > swipeLeftThreshold && myICM.accZ() > (980*0.8)) {
      // could be swiping right with controller tilted 90 degrees counter-clock wise
      client.publish("esp32/testKeaton","Swipe Left.");
    }

    // swipe right
    if (myICM.accY() < (-1*swipeLeftThreshold) && myICM.accZ() > (980*0.8)) {
      // could be swiping right with controller tilted 90 degrees clock wise (Unlikely), though this would still count as a right swipe
      client.publish("esp32/testKeaton","Swipe Right.");
    }

    // idle classifier
    float totalSquaredAcc = myICM.accX()*myICM.accX() + myICM.accY()*myICM.accY() + myICM.accZ()*myICM.accZ();
    if (totalSquaredAcc < ((980+idleThreshold)*(980+idleThreshold))) {
      //client.publish("esp32/testKeaton","Idle.");
    }


  // circular classifier "centrifugal method"

  // create a vector to store the sum of the magnitude of the Y and Z acceleration vectors
  std::vector<float> accYZ;

  // Sum the two accelerations
  float accYZ_summed = std::sqrt(myICM.accY()*myICM.accY() + scaled_accZ*scaled_accZ);
  SERIAL_PORT.print("accYZ_summed: ");
  SERIAL_PORT.print(accYZ_summed);
  SERIAL_PORT.println();

  // Set a threshold from which to determine when recording should begin
  float idle_threshold = 2000;

  // If the IMU is in motion, begin recording accYZ into the vector of data points
  bool evaluate = false;
  while (accYZ_summed > idle_threshold) {
    client.publish("esp32/testKeaton","YZ acceleration surpassed idle threshold");
    evaluate = true;
    accYZ.push_back(accYZ_summed);
    scaled_accZ = myICM.accZ() - 980;
    accYZ_summed = std::sqrt(myICM.accY()*myICM.accY() + scaled_accZ*scaled_accZ);
  }

  // When the IMU returns to idle, check to see if the YZ acceleration variance is below a small threshold, indicating a constant centrifugal force
  if (evaluate) {
    client.publish("esp32/testKeaton","evaluating centrifugal force variance");
    float mean = 0;
    for (int i = 0; i < accYZ.size(); i++) {
      mean += accYZ[i];
    }
    mean /= accYZ.size();
    float var = 0;
    for (int i = 0; i < accYZ.size(); i++) {
          var += pow(accYZ[i] - mean, 2);
    }
    accYZ.clear();
    if (var < (mean * 0.1)) {
      client.publish("esp32/testKeaton","Circular Motion.");
    }
  }
  


/*
    // circular classifier w/out phase offset consideration
    float idle_threshold = 400;
    float acc_Summed = abs(myICM.accY()) + abs(myICM.accZ());
    unsigned long lastTime = 0;
    float crossover = 300;
    float crossoverThreshold = 90;
    float varianceThreshold = 90;
    while (acc_Summed > idle_threshold) {
      // record data into a vector while Y Z acceleration is above the idle threshold
      unsigned long currentTime = millis();
      if ((abs(myICM.accY()) - crossover) < crossoverThreshold) {
        // record the elapsed time at the point when Y roughly reached the crossover point
        unsigned long elapsedTime = currentTime - lastTime;
        timestamps_Y.push_back(elapsedTime);
      }
      if ((abs(myICM.accZ()) - crossover) < crossoverThreshold) {
        // record the elapsed time at the point when Z roughly reached the crossover point
        unsigned long elapsedTime = currentTime - lastTime;
        timestamps_Z.push_back(elapsedTime);
      }

    }
    // if the timestamp vectors were populated, check their variances
    if (timestamps_Y.size() > 0 && timestamps_Z.size() > 0) {
      // calculate the mean then variance for each vector
      float meanY = 0;
      for (int i = 0; i < timestamps_Y.size(); i++) {
        meanY += timestamps_Y[i];
      }
      meanY /= timestamps_Y.size();
      float varianceY = 0;
      for (int i = 0; i < timestamps_Y.size(); i++) {
        varianceY += pow(timestamps_Y[i] - meanY, 2);
      }
      varianceY /= timestamps_Y.size();

      // now calculate the mean and variance for the Z vector
      float meanZ = 0;
      for (int i = 0; i < timestamps_Z.size(); i++) {
        meanZ += timestamps_Z[i];
      }
      meanZ /= timestamps_Z.size();
      float varianceZ = 0;
      for (int i = 0; i < timestamps_Z.size(); i++) {
        varianceZ += pow(timestamps_Z[i] - meanZ, 2);
      }
      varianceZ /= timestamps_Z.size();

      // Check if the variance in each is close enough to classify circular motion
      // For now do not consider the phase relationship between the two vectors, (since we are only using elapsed time)
      if (abs(varianceZ-varianceY) < varianceThreshold) {
        client.publish("esp32/testKeaton","Circular motion detected.");
      } else {
        client.publish("esp32/testKeaton","High Y-Z acc. but not circular.");
      }

    }
*/
    else {
      //client.publish("esp32/testKeaton","Other.");
    }
    

    //printScaledAGMT(&myICM); // This function takes into account the scale settings from when the measurement was made to calculate the values with units
    // client.publish(topic, myICM->acc.axes.x);
    client.loop();
    delay(30);
  }
  else
  {
    SERIAL_PORT.println("Waiting for data");
    client.loop();
    delay(500);
  }
}

// Below here are some helper functions to print the data nicely!

void printPaddedInt16b(int16_t val)
{
  if (val > 0)
  {
    SERIAL_PORT.print(" ");
    if (val < 10000)
    {
      SERIAL_PORT.print("0");
    }
    if (val < 1000)
    {
      SERIAL_PORT.print("0");
    }
    if (val < 100)
    {
      SERIAL_PORT.print("0");
    }
    if (val < 10)
    {
      SERIAL_PORT.print("0");
    }
  }
  else
  {
    SERIAL_PORT.print("-");
    if (abs(val) < 10000)
    {
      SERIAL_PORT.print("0");
    }
    if (abs(val) < 1000)
    {
      SERIAL_PORT.print("0");
    }
    if (abs(val) < 100)
    {
      SERIAL_PORT.print("0");
    }
    if (abs(val) < 10)
    {
      SERIAL_PORT.print("0");
    }
  }
  SERIAL_PORT.print(abs(val));
}

void printRawAGMT(ICM_20948_AGMT_t agmt)
{
  SERIAL_PORT.print("RAW. Acc [ ");
  printPaddedInt16b(agmt.acc.axes.x);
  SERIAL_PORT.print(", ");
  printPaddedInt16b(agmt.acc.axes.y);
  SERIAL_PORT.print(", ");
  printPaddedInt16b(agmt.acc.axes.z);
  SERIAL_PORT.print(" ], Gyr [ ");
  printPaddedInt16b(agmt.gyr.axes.x);
  SERIAL_PORT.print(", ");
  printPaddedInt16b(agmt.gyr.axes.y);
  SERIAL_PORT.print(", ");
  printPaddedInt16b(agmt.gyr.axes.z);
  SERIAL_PORT.print(" ], Mag [ ");
  printPaddedInt16b(agmt.mag.axes.x);
  SERIAL_PORT.print(", ");
  printPaddedInt16b(agmt.mag.axes.y);
  SERIAL_PORT.print(", ");
  printPaddedInt16b(agmt.mag.axes.z);
  SERIAL_PORT.print(" ], Tmp [ ");
  printPaddedInt16b(agmt.tmp.val);
  SERIAL_PORT.print(" ]");
  SERIAL_PORT.println();
}

void printFormattedFloat(float val, uint8_t leading, uint8_t decimals)
{
  float aval = abs(val);
  if (val < 0)
  {
    SERIAL_PORT.print("-");
  }
  else
  {
    SERIAL_PORT.print(" ");
  }
  for (uint8_t indi = 0; indi < leading; indi++)
  {
    uint32_t tenpow = 0;
    if (indi < (leading - 1))
    {
      tenpow = 1;
    }
    for (uint8_t c = 0; c < (leading - 1 - indi); c++)
    {
      tenpow *= 10;
    }
    if (aval < tenpow)
    {
      SERIAL_PORT.print("0");
    }
    else
    {
      break;
    }
  }
  if (val < 0)
  {
    SERIAL_PORT.print(-val, decimals);
  }
  else
  {
    SERIAL_PORT.print(val, decimals);
  }
}

#ifdef USE_SPI
void printScaledAGMT(ICM_20948_SPI *sensor)
{
#else
void printScaledAGMT(ICM_20948_I2C *sensor)
{
#endif
  SERIAL_PORT.print("Scaled. Acc (mg) [ ");
  printFormattedFloat(sensor->accX(), 5, 2);
  char buf[10];
  //snprintf(buf, 10, "%f", sensor->accX());
  snprintf(buf, 10, "%f", sensor->accY());   
  client.publish(topic, buf);
  SERIAL_PORT.print(", ");
  printFormattedFloat(sensor->accY(), 5, 2);
  SERIAL_PORT.print(", ");
  printFormattedFloat(sensor->accZ(), 5, 2);
  SERIAL_PORT.print(" ], Gyr (DPS) [ ");
  printFormattedFloat(sensor->gyrX(), 5, 2);
  SERIAL_PORT.print(", ");
  printFormattedFloat(sensor->gyrY(), 5, 2);
  SERIAL_PORT.print(", ");
  printFormattedFloat(sensor->gyrZ(), 5, 2);
  SERIAL_PORT.print(" ], Mag (uT) [ ");
  printFormattedFloat(sensor->magX(), 5, 2);
  SERIAL_PORT.print(", ");
  printFormattedFloat(sensor->magY(), 5, 2);
  SERIAL_PORT.print(", ");
  printFormattedFloat(sensor->magZ(), 5, 2);
  SERIAL_PORT.print(" ], Tmp (C) [ ");
  printFormattedFloat(sensor->temp(), 5, 2);
  SERIAL_PORT.print(" ]");
  SERIAL_PORT.println();
}
