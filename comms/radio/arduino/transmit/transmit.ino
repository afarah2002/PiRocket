#include <SPI.h>
#include <RF24.h>
#include <nRF24L01.h>
RF24 radio(9, 10); // CE, CSN         
const byte address[6] = "00001";     //Byte of array representing the address. This is the address where we will send the data. This should be same on the receiving side.
int button_pin = 2;
boolean button_state = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(button_pin, INPUT);
  Serial.begin(9600);
  radio.begin();                  //Starting the Wireless communication
  radio.openWritingPipe(address); //Setting the address where we will send the data
  radio.setPALevel(RF24_PA_MIN);  //You can set it as minimum or maximum depending on the distance between the transmitter and receiver.
  radio.stopListening();          //This sets the module as transmitter
}

void loop() {
  // put your main code here, to run repeatedly:
  button_state = digitalRead(button_pin);
  if(button_state == HIGH)
  {
    const char text[] = "Your Button State is HIGH";
    Serial.println(text);
    radio.write(&text, sizeof(text));                  //Sending the message to receiver
   }
  else
  {
    const char text[] = "Your Button State is LOW";
    Serial.println(text);
    radio.write(&text, sizeof(text));                  //Sending the message to receiver 
  }
  radio.write(&button_state, sizeof(button_state));  //Sending the message to receiver 
  delay(500);
}
