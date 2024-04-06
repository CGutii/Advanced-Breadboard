#include <Arduino.h>
#include <Wire.h>
#include "DFRobot_INA219.h"

#define I2C_SDA 14
#define I2C_SCL 13
DFRobot_INA219_IIC ina219(&Wire, INA219_I2C_ADDRESS1);

const int MATRIX_SIZE = 3;
const int ledPins[MATRIX_SIZE][MATRIX_SIZE] = {{2, 25, 27}, {12, 17, 32}, {26, 16, 4}};

String matrix[MATRIX_SIZE][MATRIX_SIZE];
int currentRow = 0;
bool matrixReceived = false;

void setup() {
    Serial.begin(115200);
    Wire.begin(I2C_SDA, I2C_SCL);
    for (int i = 0; i < MATRIX_SIZE; i++) {
        for (int j = 0; j < MATRIX_SIZE; j++) {
            pinMode(ledPins[i][j], OUTPUT);
            digitalWrite(ledPins[i][j], LOW);
        }
    }
    while (!ina219.begin()) {
        Serial.println("INA219 begin failed");
        delay(2000);
    }
    ina219.linearCalibrate(10000, 1000);
}

void loop() {
    if (Serial.available() > 0 && !matrixReceived) {
        processMatrix();
    }
    if (matrixReceived) {
        printSensorData();
    }
}

void processMatrix() {
  String command = Serial.readStringUntil('\n');
  command.trim();
  int col = 0, row = 0;
  int startIndex = 0, endIndex = 0;
  // Reset current row to ensure processing starts from the beginning
  currentRow = 0;
  
  // Process the entire matrix
  for (row = 0; row < MATRIX_SIZE; row++) {
    endIndex = command.indexOf(';', startIndex);
    String matrixRow = command.substring(startIndex, endIndex);
    col = 0;

    int spaceIndex = -1;
    while ((spaceIndex = matrixRow.indexOf(' ', spaceIndex + 1)) != -1) {
      String value = matrixRow.substring(0, spaceIndex);
      matrix[row][col++] = value;
      matrixRow = matrixRow.substring(spaceIndex + 1);
    }
    matrix[row][col] = matrixRow; // Last value in the row
    startIndex = endIndex + 1; // Move to the start of the next row in the command string
  }

  matrixReceived = true;
  Serial.println("MATRIX_RECEIVED");

  // After matrix processing, turn on/off LEDs
  for (row = 0; row < MATRIX_SIZE; row++) {
    for (col = 0; col < MATRIX_SIZE; col++) {
      int ledState = matrix[row][col].toInt();
      digitalWrite(ledPins[row][col], ledState ? HIGH : LOW);
      if (ledState == HIGH) {
        Serial.print("Turning on LED at pin ");
        Serial.println(ledPins[row][col]);
      }
    }
  }
}


void printSensorData() {
    Serial.print("SENSOR_DATA,");
    Serial.print(ina219.getBusVoltage_V(), 2);
    Serial.print(",");
    Serial.println(ina219.getCurrent_mA(), 1);
    delay(1000); // Adjust delay as needed
}
