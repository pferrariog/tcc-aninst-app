const int RELAY_PIN = 3;
const int COUNTER_PIN = 9;
const int REF_PIN = A0;
const int WORK_PIN = A1;

// set the voltage range for the reference electrode
const float REF_RANGE = 1.23;

// set the voltage range for the working electrode
const float WORK_RANGE = 1.23;

bool break_condition = false;
String status = "";


void setup() {
  TCCR1B = B00000001; // reset the frequency for Pin 9 of the Arduino board to 31 kHz.

  pinMode(RELAY_PIN, OUTPUT);
  pinMode(COUNTER_PIN, OUTPUT);
  pinMode(REF_PIN, OUTPUT);
  pinMode(WORK_PIN, OUTPUT);

  Serial.begin(9600);  
}

void loop() {
  if (Serial.available() > 0) {
    status = Serial.readStringUntil('\n');
    status.trim();
    
    if (status == "s") {
      break_condition = false;
      turnHotPlateRelay(status);

      // reset counter eletrode
      digitalWrite(COUNTER_PIN, 0);
      delay(100);
      digitalWrite(COUNTER_PIN, 255)
      delay(100);

      while (!monitorBlueColor()) {
        int working_voltage = analogRead(WORK_PIN);
        float working_voltage_value = (float) working_voltage * WORK_RANGE / 1023.0;

        int current = analogRead(A0);
        float current_value = (float) current * REF_RANGE / 1023.0;

        Serial.write(current_value);

        delay(100);

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
  digitalWrite(COUNTER_PIN, 0);
}

bool monitorBlueColor() {
  return false;
}
