// TCS230 pins + Arduino pins responsible
#define S0 4  
#define S1 5
#define S2 6
#define S3 7
#define sensorOut 8

const int HOT_PLATE_RELAY_PIN = 3;

int redFrequency = 0;
int greenFrequency = 0;
int blueFrequency = 0;

int redColor = 0;
int greenColor = 0;
int blueColor = 0;

void setup() {
  pinMode(HOT_PLATE_RELAY_PIN, OUTPUT);

  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  
  pinMode(sensorOut, INPUT);
  
  // Setting frequency scaling to 20%
  digitalWrite(S0,HIGH);
  digitalWrite(S1,LOW);
  
  Serial.begin(9600);
}

void loop() {
  // Turning on hot plate
  turnHotPlateRelay("start");

  // Setting RED (R) filtered photodiodes to be read
  digitalWrite(S2,LOW);
  digitalWrite(S3,LOW);
  
  // Reading the output frequency
  redFrequency = pulseIn(sensorOut, LOW);
  // Remaping the value of the RED (R) frequency from 0 to 255
  // You must replace with your own values. Here's an example: 
  // redColor = map(redFrequency, 70, 120, 255, 0);
  redColor = map(redFrequency, 70, 120, 255, 0);
  
  // Setting GREEN (G) filtered photodiodes to be read
  digitalWrite(S2,HIGH);
  digitalWrite(S3,HIGH);
  
  // Reading the output frequency
  greenFrequency = pulseIn(sensorOut, LOW);
  // Remaping the value of the GREEN (G) frequency from 0 to 255
  // You must replace with your own values. Here's an example: 
  // greenColor = map(greenFrequency, 100, 199, 255, 0);
  greenColor = map(greenFrequency, XX, XX, 255, 0);
  
  Serial.print(" G = ");
  Serial.print(greenColor);
  delay(100);
 
  // Setting BLUE (B) filtered photodiodes to be read
  digitalWrite(S2,LOW);
  digitalWrite(S3,HIGH);
  
  // Reading the output frequency
  blueFrequency = pulseIn(sensorOut, LOW);
  // Remaping the value of the BLUE (B) frequency from 0 to 255
  // You must replace with your own values. Here's an example: 
  // blueColor = map(blueFrequency, 38, 84, 255, 0);
  blueColor = map(blueFrequency, XX, XX, 255, 0);

  // Checks the blue color appearance
  if(blueColor > redColor && blueColor > greenColor){
    exitProcess()
  }
}

void turnHotPlateRelay(status) {
  if (status == "start") {
    digitalWrite(HOT_PLATE_RELAY_PIN, HIGH);
  } else {
    digitalWrite(HOT_PLATE_RELAY_PIN, LOW);
  }
} 

void exitProcess() {
  turnHotPlateRelay("stop");
  while (true){
    if (... == "start") {
      break
    }
  }
}
