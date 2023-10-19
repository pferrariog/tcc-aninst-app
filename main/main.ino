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
  // Check serial available for read commands
  if (Serial.available() > 0 && Serial.readString() == "start") {
    // Turning on hot plate
    turnHotPlateRelay("start");
  }

  // Monitor the process until stop at blue color shows up
  while (!monitorBlueColor())
  {
    // TODO keep printing constantly data to python catches it
  }
  
  exitProcess()
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
    if (Serial.readString() == "start") {
      break
    }
  }
}

void monitorBlueColor() {
  // RED (R) filtered photodiodes
    digitalWrite(S2,LOW);
    digitalWrite(S3,LOW);
    
    redFrequency = pulseIn(sensorOut, LOW);
    redColor = map(redFrequency, 70, 120, 255, 0);
    
    // GREEN (G) filtered photodiodes
    digitalWrite(S2,HIGH);
    digitalWrite(S3,HIGH);
    
    greenFrequency = pulseIn(sensorOut, LOW);
    greenColor = map(greenFrequency, 100, 199, 255, 0);
  
    // BLUE (B) filtered photodiodes
    digitalWrite(S2,LOW);
    digitalWrite(S3,HIGH);
    
    blueFrequency = pulseIn(sensorOut, LOW);
    blueColor = map(blueFrequency, 38, 84, 255, 0);

    // Checks the blue color appearance
    if(blueColor > redColor && blueColor > greenColor){
      return true
    }

    return false
}