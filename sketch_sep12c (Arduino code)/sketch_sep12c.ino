#include <SPI.h>
#include <MFRC522.h>

// Define the pins used for the RFID reader
#define SS_PIN 10
#define RST_PIN 9

// Create an instance of the MFRC522 reader
MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  // Start serial communication at 9600 baud rate
  Serial.begin(9600);
  // Initialize the SPI bus
  SPI.begin();
  // Initialize the MFRC522 reader
  mfrc522.PCD_Init();
  Serial.println("Arduino is ready. Please scan a card.");
}

void loop() {
  // Look for a new card
  if ( ! mfrc522.PICC_IsNewCardPresent()) {
    return; // If no card is found, restart the loop
  }

  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) {
    return; // If card cannot be read, restart the loop
  }

  // Create a string to hold the UID
  String uidString = "";
  // Loop through the bytes of the UID
  for (byte i = 0; i < mfrc522.uid.size; i++) {
     // Add a space between bytes and format as hexadecimal
     uidString += (mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
     uidString += String(mfrc522.uid.uidByte[i], HEX);
  }
  // Remove leading/trailing spaces
  uidString.trim();
  
  // Print the UID to the serial port
  Serial.println(uidString);
  
  // Halt PICC
  mfrc522.PICC_HaltA();
  // Stop encryption on PCD
  mfrc522.PCD_StopCrypto1();
  
  delay(1000); // Wait a second before reading another card
}
