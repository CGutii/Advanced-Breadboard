#include <Arduino.h>

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

    if (command == "request_data") {
      sendMultimeterData();
      matrixReceived = false;
      currentRow = 0;
      return;
  }

  }
}

void sendMultimeterData() {
  // Make sure you have included and configured the library for the digital multimeter
  float voltage = ina219.getBusVoltage_V();
  float current_mA = ina219.getCurrent_mA();
  float power_mW = ina219.getPower_mW();

  Serial.print("Voltage: ");
  Serial.print(voltage);
  Serial.print("V, Current: ");
  Serial.print(current_mA);
  Serial.print("mA, Power: ");
  Serial.print(power_mW);
  Serial.println("mW");
}


