#include <Wire.h>
#include "DFRobot_INA219.h"

DFRobot_INA219_IIC ina219(&Wire, INA219_I2C_ADDRESS4);

const int MATRIX_SIZE = 3;
const int ledPins[MATRIX_SIZE][MATRIX_SIZE] = {
  {2, 27, 12},
  {17, 16, 4},
  {26, 25, 32}
};

String matrix[MATRIX_SIZE][MATRIX_SIZE];
int currentRow = 0;
bool matrixReceived = false;

void setup() {
  Serial.begin(9600);
  while (!Serial); // Wait for Serial to be ready

  Wire.begin(); // Initialize I2C communication
  while (!ina219.begin()) {
    Serial.println("INA219 begin failed");
    delay(2000);
  }

  for (int i = 0; i < MATRIX_SIZE; i++) {
    for (int j = 0; j < MATRIX_SIZE; j++) {
      pinMode(ledPins[i][j], OUTPUT);
      digitalWrite(ledPins[i][j], LOW); // Ensure LEDs are off initially
    }
  }
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    int col = 0;
    int index = 0;
    while (index != -1 && col < MATRIX_SIZE) {
      index = command.indexOf(' ', index + 1);
      String value = index != -1 ? command.substring(0, index) : command;
      matrix[currentRow][col++] = value;
      command = index != -1 ? command.substring(index + 1) : "";
    }
    currentRow++;

    if (currentRow == MATRIX_SIZE) {
      matrixReceived = true;
      currentRow = 0; // Reset for next reception
    }

    if (matrixReceived) {
      Serial.println("Matrix Received:");
      for (int i = 0; i < MATRIX_SIZE; i++) {
        for (int j = 0; j < MATRIX_SIZE; j++) {
          Serial.print(matrix[i][j] + " ");
          int ledState = matrix[i][j].toInt();
          digitalWrite(ledPins[i][j], ledState);
          if (ledState) {
            Serial.print("Turning on LED at pin ");
            Serial.println(ledPins[i][j]);
          }
        }
        Serial.println();
      }
      
      // Read sensor data after the matrix is processed
      float busVoltage = ina219.getBusVoltage_V();
      float shuntVoltage = ina219.getShuntVoltage_mV();
      float current_mA = ina219.getCurrent_mA();
      float power_mW = ina219.getPower_mW();
  
      // Send sensor data to Pi
      Serial.print("Sensor data: ");
      Serial.print(busVoltage); Serial.print("V, ");
      Serial.print(shuntVoltage); Serial.print("mV, ");
      Serial.print(current_mA); Serial.print("mA, ");
      Serial.print(power_mW); Serial.println("mW");

      matrixReceived = false; // Reset flag for next matrix
    }
  }
}
