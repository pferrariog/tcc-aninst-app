const int RELAY_PIN = 3;
const int COUNTER_PIN = 9;
const int REF_PIN = A0;
const int WORK_PIN = A1;

// TCS230 or TCS3200 pins wiring to Arduino
#define S0 4
#define S1 5
#define S2 6
#define S3 7
#define sensorOut 8

// Stores frequency read by the photodiodes
int redFrequency = 0;
int greenFrequency = 0;
int blueFrequency = 0;

// Stores the red. green and blue colors
int redColor = 0;
int greenColor = 0;
int blueColor = 0;

bool break_condition = false;
String status = "";
float potential = 96; // 96 de 0 a 1023 == 0.6V

const float R_REF = 68;
float current_in_mA;


void setup() {
  TCCR1B = B00000001; // reset the frequency for Pin 9 of the Arduino board to 31 kHz.
  Serial.begin(9600);

  // pinMode(RELAY_PIN, OUTPUT);
  pinMode(COUNTER_PIN, OUTPUT);
  pinMode(REF_PIN, OUTPUT);
  pinMode(WORK_PIN, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    status = Serial.readStringUntil('\n');
    status.trim();

    if (status == "s") {
      break_condition = false;
      // turnHotPlateRelay(status);

      // reset counter eletrode
      digitalWrite(COUNTER_PIN, 0);
      delay(100);
      digitalWrite(COUNTER_PIN, 255);
      delay(100);

      analogWrite(WORK_PIN, potential);
      delay(1000);
      analogWrite(WORK_PIN, 0);

      // lê a corrente fluindo pelo eletrodo de trabalho
      float current_value = (float) analogRead(REF_PIN);

      // calcula a tensão do eletrodo contra-eletrodo para compensar a corrente
      float counter_voltage = -current_value / R_REF;

      // aplica a tensão do eletrodo contra-eletrodo
      analogWrite(COUNTER_PIN, counter_voltage);

      current_value = (float) analogRead(REF_PIN);
      current_in_mA = current_value * (1000 / 1023);
      Serial.println(current_in_mA); // corrente de início

      while (!monitorBlueColor()) {
        analogWrite(WORK_PIN, potential);
        int current = analogRead(REF_PIN);
        float current_value = (float) current * (1000 / 1023);
        Serial.println(current);
        delay(100);

        if (Serial.available() > 0 && status != "s") {
          break_condition = true;
          break;
        }
      }
    }
  }
  if (status != "s" && status != "p") {
    float ref_potential = status.toFloat();
    potential = map(ref_potential, 0, 5, 0, 1023);
  }
  if (break_condition) {
    exitProcess();
    break_condition = false;
  }
}

void turnHotPlateRelay(String status) {
  if (status == "s") {
    digitalWrite(RELAY_PIN, HIGH);
  }
  else {
    digitalWrite(RELAY_PIN, LOW);
  }
}

void exitProcess() {
  turnHotPlateRelay("p");
  digitalWrite(COUNTER_PIN, 0);
  Serial.print("end");
}

bool monitorBlueColor() {
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
    return true;
  }
  return false;
}
