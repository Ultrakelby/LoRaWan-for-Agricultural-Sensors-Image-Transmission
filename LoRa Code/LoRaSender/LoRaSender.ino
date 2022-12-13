#include <SPI.h>
#include <LoRa.h>
#include <string>
#include <HardwareSerial.h>
#include <string>
#include <iostream>
using namespace std;

#define SCK 5
#define MISO 19
#define MOSI 27
#define SS 18
#define RST 14
#define DIO0 26

// Define pins used for RTS/CTS 
const int RTS = 21; // Output to CTS
const int CTS = 22; // Input from RTS

//packet counter
int counter = 0;
//Data array Counter
int i = 0;
//Data from pico
String serialIn; // Set and wipe variable

int CTS_State = LOW; // Variable for Reading CTS status

void setup() {
  Serial.begin(9600);

  //SPI LoRa pins
  SPI.begin(SCK, MISO, MOSI, SS);
  //setup LoRa transceiver module
  LoRa.setPins(SS, RST, DIO0);

  if (!LoRa.begin(915E6)) {
   Serial.print("Starting LoRa failed!");
  }
  else{
    Serial.println("Sarting LoRa Success");
  }

Serial2.begin(9600,SERIAL_8N1,16,17);
  //while (!Serial);
  Serial.println("LoRa Sender");

  pinMode(RTS, OUTPUT); // Initialize the RTS pin as Output
  pinMode(CTS, INPUT_PULLUP);  // Initialize the CTS pin as INPUT - Active HIGH

  Serial.print("CTS State = ");
  Serial.println(CTS_State);
}

void loop() {
  CTS_State = digitalRead(CTS);

  if (CTS_State == HIGH){ // Receive data from the Pico
    Serial.println("Receiving from pico");

    // Waits for each packet to send via the Lora before reactivating UART 
    digitalWrite(RTS, HIGH); // Set RTS to high
    serialIn = Serial2.readStringUntil('\n'); // Takes in bytes
    digitalWrite(RTS, LOW); // Set RTS to low 
    
  
    Serial.print("Input From Pico => ");
    Serial.println(serialIn); // Print the result 
    
    Serial.print("Sending packet: ");
    Serial.println(counter);

    //Send LoRa packet to receiver
    LoRa.beginPacket();
    LoRa.print(serialIn);
    LoRa.endPacket();

    Serial.println();
    counter++;
    delay(10);
  } 
}