#include <Arduino.h>

#define redLed 4 

String command;
bool matrixReceived = false;
const int MATRIX_SIZE = 3;
String matrix[MATRIX_SIZE][MATRIX_SIZE];
int currentRow = 0;

void setup() {
  Serial.begin(9600);
  pinMode(redLed, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    command = Serial.readStringUntil('\n');
    command.trim();

    if (!matrixReceived && currentRow < MATRIX_SIZE) {
      matrixReceived = true;
      currentRow = 0;
      
      int startIndex = 0;
      int endIndex = command.indexOf(';');
      while (endIndex != -1 && currentRow < MATRIX_SIZE) {
        String row = command.substring(startIndex, endIndex);
        int col = 0;
        int spaceIndex = row.indexOf(' ');
        while (spaceIndex != -1) {
          matrix[currentRow][col++] = row.substring(0, spaceIndex);
          row = row.substring(spaceIndex + 1);
          spaceIndex = row.indexOf(' ');
        }
        matrix[currentRow][col] = row;
        
        startIndex = endIndex + 1;
        endIndex = command.indexOf(';', startIndex);
        currentRow++;
      }
    }

    if (matrixReceived) {
      Serial.println("Matrix Received:");
      for (int i = 0; i < MATRIX_SIZE; i++) {
        for (int j = 0; j < MATRIX_SIZE; j++) {
          Serial.print(matrix[i][j] + " ");
        }
        Serial.println();
      }
      Serial.println("Received on the ESP");
      digitalWrite(redLed, HIGH);
      delay(500);
      digitalWrite(redLed, LOW);
      
      matrixReceived = false;
      currentRow = 0;
    }
  }
}
