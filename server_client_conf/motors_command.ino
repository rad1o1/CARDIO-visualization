/* This code controls the stepper motors and the LED intensity
 * according to the data received from the UART (RX, TX) (Controller) or the USB (e.g. Raspberry Pi)
 * All 6 motors share the same stepper motor pins, but only one
 * is activated depending on the status of the Enable pin of the driver
 * Data format: "50X," where 50 is the speed and X is the axis
 * X: X axis, Y: Y axis, Z: Z axis, C: camera stage, R: rotation, T: tilt 
 * The data is executed after a "," (comma) is received
 */

// Arduino board: Adafruit ItsyBitsy32u4 5V 

#include <AccelStepper.h> // Library to control stepper motors // Copyright (C) 2010-2018 Mike McCauley

AccelStepper motors(AccelStepper::FULL4WIRE, 2, 3, 4, 5); // stepper motors

//    #include <Adafruit_NeoPixel.h> // Library to control the optional status LED


/////////////////

#define LEDPWM 6 // High-power illumination LED PWM control pin 

#define RED 11
#define BLU 10
#define GRN 9

#define EnableX 7
#define EnableY 8
#define EnableZ 12


const int stepsPerRevolution = 4096; //set according to the specs of the stepper motor
String receivedString; //incoming data from the serial ports (USB or UART)
int stepperSpeed;
char state; //variable to define the active stepper motor, X, Y, Z
int LEDintensity;

// Adafruit_NeoPixel pixel(1, NeopixelPin, NEO_GRB + NEO_KHZ800);


void setup() {

   Serial.begin(57600); // USB, Raspberry Pi
  
   pinMode(LEDPWM, OUTPUT);

   analogWrite(LEDPWM, 0); // initialize the LED intensity to 0% 
  /* PWM of the LED driver (RCD-24-0.70/PL/B, Recom) used in this project
   * works in the opposite direction, i.e. 255 is for 0% and 0 for 100% intensity
   */
  
  /*pixel.begin();
  *pixel.setPixelColor(0, pixel.Color(0, 0, 50));
  *pixel.show();
  */
  
  

   pinMode(RED, OUTPUT);
   pinMode(GRN, OUTPUT);
   pinMode(BLU, OUTPUT);
   pinMode(EnableX, OUTPUT);
   pinMode(EnableY, OUTPUT);
   pinMode(EnableZ, OUTPUT);

   motors.setMaxSpeed(1000);

}

void loop() {

//// data from USB (Raspberry Pi)

  if (Serial.available() > 0) {
    char data = Serial.read();
    if (data == ',') {

      if (receivedString.length() > 1) {
        int stepperSpeed = receivedString.toInt();
        motors.setSpeed(stepperSpeed);

        if (receivedString.indexOf('X') > 0) {
          state = 'X';
        }
        if (receivedString.indexOf('Y') > 0) {
          state = 'Y';
        }
        if (receivedString.indexOf('Z') > 0) {
          state = 'Z';
        }
        if (receivedString.indexOf('L') > 0) {
          LEDintensity = map(stepperSpeed, 0, 20, 0, 255);
          analogWrite(LEDPWM, LEDintensity);
        }
        if (receivedString.indexOf('O') > 0) {
          state = 'O';
        }
        receivedString = "";
      }
    }
    else {
      receivedString += data;
    }
  }

///// RUN STEPPER MOTORS, only one runs at a given time

  if (state == 'X') {
    
    digitalWrite(EnableX, HIGH);
    motors.runSpeed();
  }

  if (state == 'Y') {

    digitalWrite(EnableY, HIGH);
    motors.runSpeed();
  }

  if (state == 'Z') {

    digitalWrite(EnableZ, HIGH);
    motors.runSpeed();
  }

// STOP all stepper motors 

  if (state == 'O') {
    motors.stop();
    digitalWrite(EnableX, LOW);
    digitalWrite(EnableY, LOW);
    digitalWrite(EnableZ, LOW);
  }

}