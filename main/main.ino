const int HOT_PLATE_RELAY_PIN = 3;
const int PWM_PIN = 9;
const int CIRCUIT_PIN_0 = A0;
const int CIRCUIT_PIN_1 = A1;

bool break_condition = false;
String status = "";


void setup() {
  pinMode(HOT_PLATE_RELAY_PIN, OUTPUT);
  pinMode(PWM_PIN, OUTPUT);
  Serial.begin(9600);  
}

void loop() {
  if (Serial.available() > 0) {
    status = Serial.readStringUntil('\n');
    status.trim();
    
    if (status == "s") {
      break_condition = false;
      digitalWrite(10, HIGH); // EXAMPLE 
      turnHotPlateRelay(status);
      while (!monitorBlueColor()) {
        
        Serial.write(analogRead(CIRCUIT_PIN_0)); // EXAMPLE

        if (Serial.available() > 0 && status != "s") {
          break_condition = true;
          break;
        }
      }
    }
  }
  if (break_condition) {
    exitProcess();
    break_condition = false;
  }
}

void turnHotPlateRelay(String status) {
  if (status == "s") {
    digitalWrite(HOT_PLATE_RELAY_PIN, HIGH);
  }
  else {
    digitalWrite(HOT_PLATE_RELAY_PIN, LOW);
  }
}

void exitProcess() {
  turnHotPlateRelay("p");
  // stop other circuit elements
}

bool monitorBlueColor() {
  return false;
}
