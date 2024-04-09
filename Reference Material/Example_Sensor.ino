#include <Wire.h>
#include "DFRobot_INA219.h"

// LEDs......GPIO#
#define vLed1 12
#define iLed2 27

#define I2C_SDA 14
#define I2C_SCL 13

DFRobot_INA219_IIC ina219(&Wire, INA219_I2C_ADDRESS1);

// Revise the following two parameters according to actual reading of the INA219 and the multimeter
// for linear calibration
float ina219Reading_mA = 10000;
float extMeterReading_mA = 1000;

void setup(void) {
    pinMode(vLed1, OUTPUT);
    pinMode(iLed2, OUTPUT);

    Serial.begin(115200);
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

void loop(void) {
    Serial.print("BusVoltage:   ");
    Serial.print(ina219.getBusVoltage_V(), 2);
    Serial.println("V");

    if (ina219.getBusVoltage_V() > 0) {
        digitalWrite(vLed1, HIGH);
    }

    Serial.print("ShuntVoltage: ");
    Serial.print(ina219.getShuntVoltage_mV(), 3);
    Serial.println("mV");

    Serial.print("Current:      ");
    Serial.print(ina219.getCurrent_mA(), 1);
    Serial.println("mA");

    if (ina219.getCurrent_mA() > 0) {
        digitalWrite(iLed2, HIGH);
    } else {
        digitalWrite(iLed2, LOW); // Turn off LED if current is not greater than 0
    }

    Serial.print("Power:        ");
    Serial.print(ina219.getPower_mW(), 1);
    Serial.println("mW");
    Serial.println("");

    delay(1000);
}
