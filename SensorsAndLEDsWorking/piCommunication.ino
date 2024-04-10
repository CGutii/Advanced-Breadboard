#include <Arduino.h>
#include <Wire.h>
#include "DFRobot_INA219.h"

// redefined I2C Pins
#define I2C_SDA 14
#define I2C_SCL 13
//#define MATRIX_SIZE 9
#define led1 2
#define led2 25
#define led3 27
#define led4 12
#define led5 17
#define led6 32
#define led7 26
#define led8 16
#define led9 4

//int ledPins[MATRIX_SIZE] = {2, 4, 5, 18, 19, 21, 22, 23, 25};

//int currentRow = 0;

// ADDRESS1 with the PCB, ADDRESS4 with the dev board
DFRobot_INA219_IIC ina219(&Wire, INA219_I2C_ADDRESS1);

// for linear calibration
float ina219Reading_mA = 10000;
float extMeterReading_mA = 1000;

//String matrix[MATRIX_SIZE][MATRIX_SIZE];      // Matrix to store the received values
//int currentRow = 0;                           // Current row being processed
bool matrixReceived = false;                  // Flag to indicate if matrix is fully received

void setup() {
  Serial.begin(115200);

   // Initialize the LED pins
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  pinMode(led4, OUTPUT);
  pinMode(led5, OUTPUT);
  pinMode(led6, OUTPUT);
  pinMode(led7, OUTPUT);
  pinMode(led8, OUTPUT);
  pinMode(led9, OUTPUT);

  //pinMode(ledPins[i][j], OUTPUT);
  digitalWrite(led1, LOW); // Turn off all LEDs initially
  digitalWrite(led2, LOW); // Turn off all LEDs initially
  digitalWrite(led3, LOW); // Turn off all LEDs initially
  digitalWrite(led4, LOW); // Turn off all LEDs initially
  digitalWrite(led5, LOW); // Turn off all LEDs initially
  digitalWrite(led6, LOW); // Turn off all LEDs initially
  digitalWrite(led7, LOW); // Turn off all LEDs initially
  digitalWrite(led8, LOW); // Turn off all LEDs initially
  digitalWrite(led9, LOW); // Turn off all LEDs initially

  

  while (!Serial);
    Wire.begin(I2C_SDA, I2C_SCL); // Initialize I2C communication

    while (!ina219.begin()) {
        Serial.println("INA219 begin failed");
        delay(2000);
    }

    // Linear calibration b4 and after calibration 
    ina219.linearCalibrate(ina219Reading_mA,extMeterReading_mA);
    //Serial.println();
}


void loop() {
  
  if (Serial.available() > 0) {
    String information = Serial.readStringUntil('\n');
    //Serial.println(information);
    information.trim();

    Serial.println(information);

    // if information is matrix then process and turn on LEDS
    if(matrixReceived == false){
      //Serial.println(information);
      processMatrix(information);
    }

    //if info is a char (get sensor stuff)
    if (information == "GET_SENSOR_DATA"){
      //Serial.end();
      GetSensorData();
    }

    if (information == "RESET_PINS") {
      resetPins();
    }

  }
}

// serial print sensor data
void GetSensorData() {
  //Serial.begin(115200);
  // send request to send data
  //Serial.write("Ready for Sensor Data?");

  //Serial.print("BusVoltage:   ");
  //int voltage = (int)ina219.getBusVoltage_V();
  //int current = (int)ina219.getCurrent_mA();
  //Serial.write(voltage);
  //Serial.write(current);
  Serial.flush();
  

  float busVoltage = ina219.getBusVoltage_V();
  float current = ina219.getCurrent_mA();

  
  // Convert float to string
  String busVoltageString = String(busVoltage, 2); // 2 decimal places
  String currentString = String(current, 2); // 2 decimal places
  
  // Write the string over serial
  Serial.print(busVoltageString);
  Serial.print("V ");
  Serial.print(currentString);
  Serial.print("mA");

   //Serial.write(ina219.getBusVoltage_V(), 2);
   //Serial.write("V   ");

   //Serial.print("Current:      ");
   //Serial.write(ina219.getCurrent_mA(), 1);
   //Serial.write("mA");
  //delay(1000);
    //Serial.println("here");
  
}

void processMatrix(String information) {
  // Parse the received information into individual LED states
  //Serial.print("Info printing:");
 // Serial.print(information);
  
  // Iterate through the input string and control each LED accordingly
  for (int col = 0; col < 9; col++) {
    // Find the index of the next space character
    int index = information.indexOf(' ');
    
    // Extract the substring representing the state of the current LED
    String value = (index != -1) ? information.substring(0, index) : information;
    
    // Convert the string to an integer representing the LED state
    int ledState = value.toInt();
    
    // Determine whether to turn the LED on or off based on the LED state
    digitalWrite(getLedPin(col), (ledState == 1) ? HIGH : LOW);
    
    // Print the LED state (for debugging)
    //Serial.println(ledState);
    
    // Update the input string for the next LED
    information = (index != -1) ? information.substring(index + 1) : "";
  }
  
  // Print a message indicating the end of LED processing
  //Serial.println('a');
  
  // now send the ack to the circuit_simulator
  //Serial.println(information);
  matrixReceived = true;
}

// Function to get the pin number of the LED corresponding to the specified index
int getLedPin(int index) {
  switch (index) {
    case 0: return led1;
    case 1: return led2;
    case 2: return led3;
    case 3: return led4;
    case 4: return led5;
    case 5: return led6;
    case 6: return led7;
    case 7: return led8;
    case 8: return led9;
    default: return -1; // Invalid index
  }
}

void resetPins() {
  digitalWrite(led1, LOW);
  digitalWrite(led2, LOW);
  digitalWrite(led3, LOW);
  digitalWrite(led4, LOW);
  digitalWrite(led5, LOW);
  digitalWrite(led6, LOW);
  digitalWrite(led7, LOW);
  digitalWrite(led8, LOW);
  digitalWrite(led9, LOW);
}

