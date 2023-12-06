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
int potential = 33;
float desired_potential = 0.6;

float end_time = 150.00;

void setup() {
  TCCR1B = B00000001; // reset the frequency for Pin 9 of the Arduino board to 31 kHz.
  Serial.begin(9600);
  Serial.flush();

  pinMode(COUNTER_PIN, OUTPUT);
  pinMode(REF_PIN, INPUT);
  pinMode(WORK_PIN, INPUT);
}

void loop() {
  if (Serial.available() > 0) {
    status = Serial.readStringUntil('\n');
    status.trim();

    if (status == "s") {
      break_condition = false;

      // reset counter eletrode
      analogWrite(COUNTER_PIN, 0);
      delay(500);

      // lê a corrente de circuito aberto
      float work_voltage = analogRead(WORK_PIN) * 4.8828; // 5.0/1023.0 * 1000 (mV) - conversion factor
      Serial.println((work_voltage / 0.202), 6); // shunt resistor value according to reference (0.202 mOhm)

      // lê a voltagem de referencia
      float ref_voltage = analogRead(REF_PIN) * 4.8828; // mA
      Serial.println(ref_voltage, 6);

      Serial.println(work_voltage_zero - ref_zero, 6);
      delay(500);

      float start_time = millis();

      while (millis() - start_time < 15.00) // wait for cathodic current goes away

      // while (!monitorBlueColor())
      while (millis() - start_time < end_time) {
        analogWrite(COUNTER_PIN, potential);

        work_voltage = analogRead(WORK_PIN) * 4.8828;
        Serial.println(work_voltage / 0.202, 6); // check if works with 0.202

        ref_voltage = analogRead(REF_PIN) * 4.8828;;
        Serial.println(ref_voltage, 6);

        float cell_potential = work_voltage - ref_voltage;
        Serial.println(cell_potential, 6);
        delay(200);
      }
      break_condition = true;
    }
  }
  if (status != "" && status != "s" && status != "p") {
    float ref_potential = status.toFloat();
    potential = mapfloat(ref_potential, 0, 5, 0, 1023);
    potential = (int) potential;
    Serial.println(potential);
  }
  if (break_condition) {
    exitProcess();
    break_condition = false;
  }
}

void exitProcess() {
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

float mapfloat(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
