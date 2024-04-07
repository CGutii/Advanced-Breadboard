#include <Arduino.h>
#include <Wire.h>
#include "DFRobot_INA219.h"

#define I2C_SDA 14
#define I2C_SCL 13

const int MATRIX_SIZE = 3;
// Define the LED pins based on the matrix position
const int ledPins[MATRIX_SIZE][MATRIX_SIZE] = {
  {2, 25, 27},
  {12, 17, 32},
  {26, 16, 4}
};

//remember to adjust this value according to what board we are using
DFRobot_INA219_IIC ina219(&Wire, INA219_I2C_ADDRESS1);

// Revise the following two parameters according to actual reading of the INA219 and the multimeter
// for linear calibration
float ina219Reading_mA = 10000;
float extMeterReading_mA = 1000;

String matrix[MATRIX_SIZE][MATRIX_SIZE]; // Matrix to store the received values
int currentRow = 0; // Current row being processed
bool matrixReceived = false; // Flag to indicate if matrix is fully received

void setup() {
  Serial.begin(115200); // Begin serial communication at 9600 baud rate
  
  // Initialize the LED pins
  for (int i = 0; i < MATRIX_SIZE; i++) {
    for (int j = 0; j < MATRIX_SIZE; j++) {
      pinMode(ledPins[i][j], OUTPUT);
      digitalWrite(ledPins[i][j], LOW); // Turn off all LEDs initially
    }
  }

  while (!Serial);

    Wire.begin(I2C_SDA, I2C_SCL); // Initialize I2C communication

    while (!ina219.begin()) {
        Serial.println("INA219 begin failed");
        delay(2000);
    }

    // Linear calibration b4 and after calibration 
    ina219.linearCalibrate(ina219Reading_mA,extMeterReading_mA);
    Serial.println();
  
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    // Parse the received command into the matrix
    int col = 0;
    int index = 0;
    while (index != -1 && col < MATRIX_SIZE) {
      index = command.indexOf(' ');
      String value = (index != -1) ? command.substring(0, index) : command;
      matrix[currentRow][col++] = value;
      command = (index != -1) ? command.substring(index + 1) : "";
    }

    // Turn on/off the LEDs for the current row
    for (int col = 0; col < MATRIX_SIZE; col++) {
      int ledState = matrix[currentRow][col].toInt();
      digitalWrite(ledPins[currentRow][col], ledState);
      if (ledState == HIGH) {
        Serial.print("Turning on LED at pin ");
        Serial.println(ledPins[currentRow][col]);
      }
    }

    currentRow++;
    
    // Check if the last row has been processed
    if (currentRow == MATRIX_SIZE) {
      //matrixReceived = true;
      Serial.println("Entire matrix received on ESP.");
      // Reset for the next matrix
      currentRow = 0;
      //printSensorData();  // Continuously send sensor data after matrix processing

    }

    //this should print out the sensor info
    //printSensorData();
  }

  //if (matrixReceived) {
    //Serial.println("MATRIX_RECEIVED");  // Confirm matrix reception
    //printSensorData();  // Continuously send sensor data after matrix processing
  //}
  // New - Check if it's time to send sensor data without blocking
  static unsigned long lastSensorDataMillis = 0;
  if (millis() - lastSensorDataMillis > 3000) { // Adjust as needed
    printSensorData();
    lastSensorDataMillis = millis();
  }
}

void printSensorData() {
  while(1){
    Serial.print("Voltage:");
    Serial.print(ina219.getBusVoltage_V(), 2);
    Serial.print("  Current:");
    Serial.print(ina219.getCurrent_mA(), 1);
    delay(3000); // Adjust delay as needed for continuous data sending
  }
}
