#include <Arduino.h>

// Global variables to store sensor data
float busVoltage = 0;
float shuntVoltage = 0;
float current_mA = 0;
float power_mW = 0;

const int MATRIX_SIZE = 3;
// Define the LED pins based on the matrix position
const int ledPins[MATRIX_SIZE][MATRIX_SIZE] = {
  {2, 27, 12},
  {17, 16, 4},
  {26, 25, 32}
};

String matrix[MATRIX_SIZE][MATRIX_SIZE]; // Matrix to store the received values
int currentRow = 0; // Current row being processed
bool matrixReceived = false; // Flag to indicate if matrix is fully received

void setup() {
  Serial.begin(9600); // Begin serial communication at 9600 baud rate
  
  // Initialize the LED pins
  for (int i = 0; i < MATRIX_SIZE; i++) {
    for (int j = 0; j < MATRIX_SIZE; j++) {
      pinMode(ledPins[i][j], OUTPUT);
      digitalWrite(ledPins[i][j], LOW); // Turn off all LEDs initially
    }
  }
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
      matrixReceived = true;
      Serial.println("Entire matrix received on ESP.");
      // Reset for the next matrix
      currentRow = 0;
    }

      if (matrixReceived) {
      // Read sensor data
      busVoltage = ina219.getBusVoltage_V();
      shuntVoltage = ina219.getShuntVoltage_mV();
      current_mA = ina219.getCurrent_mA();
      power_mW = ina219.getPower_mW();
    
      // Send sensor data to Pi
      Serial.print(busVoltage); Serial.print(",");
      Serial.print(shuntVoltage); Serial.print(",");
      Serial.print(current_mA); Serial.print(",");
      Serial.println(power_mW);

      matrixReceived = false; // Reset flag for next matrix
    }
  }
}
