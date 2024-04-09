#include <Arduino.h>
#include <Wire.h>
#include "DFRobot_INA219.h"

// redefined I2C Pins
#define I2C_SDA 14
#define I2C_SCL 13

const int MATRIX_SIZE = 3;

// define the LED pins based on the matrix position
const int ledPins[MATRIX_SIZE][MATRIX_SIZE] = {
  {2, 25, 27},
  {12, 17, 32},
  {26, 16, 4}
};

// ADDRESS1 with the PCB, ADDRESS4 with the dev board
DFRobot_INA219_IIC ina219(&Wire, INA219_I2C_ADDRESS1);

// for linear calibration
float ina219Reading_mA = 10000;
float extMeterReading_mA = 1000;

String matrix[MATRIX_SIZE][MATRIX_SIZE];      // Matrix to store the received values
int currentRow = 0;                           // Current row being processed
bool matrixReceived = false;                  // Flag to indicate if matrix is fully received

void setup() {
  Serial.begin(115200);
  
  // Turn LEDs off
  for (int i = 0; i < MATRIX_SIZE; i++) {
    for (int j = 0; j < MATRIX_SIZE; j++) {
      pinMode(ledPins[i][j], OUTPUT);
      digitalWrite(ledPins[i][j], LOW);
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
    String information = Serial.readStringUntil('\n');
    information.trim();

    // if information is matrix then process and turn on LEDS
    if(matrixReceived == false)
    processMatrix(information);

    //if info is a char (get sensor stuff)
    if (information == "GET_SENSOR_DATA")
    GetSensorData();

  }
}

// serial print sensor data
void GetSensorData() {
  // send request to send data
  Serial.print("Ready for Sensor Data?");

  Serial.print("BusVoltage:   ");
  Serial.print(ina219.getBusVoltage_V(), 2);
  Serial.println("V");

  Serial.print("Current:      ");
  Serial.print(ina219.getCurrent_mA(), 1);
  Serial.println("mA");
  //delay(1000);
    //Serial.println("here");
  
}

void processMatrix(String information){

// Parse the received information into the matrix
    int col = 0;
    int index = 0;
    while (index != -1 && col < MATRIX_SIZE) {
      index = information.indexOf(' ');
      String value = (index != -1) ? information.substring(0, index) : information;
      matrix[currentRow][col++] = value;
      information = (index != -1) ? information.substring(index + 1) : "";
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
      matrixReceived = true;
      Serial.println("Entire matrix received on ESP.");
      // Reset for the next matrix
      currentRow = 0;
    }

  //now send the ack to the circuit_simulator
  Serial.println('2');
  matrixReceived = true;
}

