#include <Arduino.h>

// Assuming redLed is connected to GPIO 4 as an example. Adjust according to your setup.
#define redLed 4 

String command;
bool matrixReceived = false;
const int MATRIX_SIZE = 3; // Assuming a 3x3 matrix
String matrix[MATRIX_SIZE];
int currentRow = 0;

void setup() {
  Serial.begin(9600); // Initialize serial communication at 9600 baud rate
  pinMode(redLed, OUTPUT); // Set redLed as an OUTPUT
}

void loop() {
  if (Serial.available() > 0) {
    command = Serial.readStringUntil('\n'); // Read the incoming data until newline
    command.trim(); // Trim any whitespace

    if (!matrixReceived) {
      // Store each line of the matrix until it's fully received
      if (currentRow < MATRIX_SIZE) {
        matrix[currentRow] = command;
        currentRow++;
      }
      if (currentRow == MATRIX_SIZE) {
        matrixReceived = true;
      }
    }

    // If the matrix is fully received, print it out and send a confirmation message
    if (matrixReceived) {
      Serial.println("Matrix Received:");
      for (int i = 0; i < MATRIX_SIZE; i++) {
        Serial.println(matrix[i]);
      }
      Serial.println("We got your matrix!"); // Send confirmation message
      matrixReceived = false; // Reset for the next matrix
      currentRow = 0; // Reset row counter
    }
  }
}
