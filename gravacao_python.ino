const int buttonPin = 8;
bool buttonState = false;
bool lastButtonState = false;
int clickCount = 0;

int ledVerde = 2;
int ledAmareloeq = 5;
int ledVerdeeq = 6;
int ledVermelhoeq = 7;

char comando;
bool gravando = false;

void setup() {
  pinMode(buttonPin, INPUT);
  pinMode(ledVerde, OUTPUT);
  pinMode(ledAmareloeq, OUTPUT);
  pinMode(ledVerdeeq, OUTPUT);
  pinMode(ledVermelhoeq, OUTPUT);

  Serial.begin(9600);
  lastButtonState = digitalRead(buttonPin) == LOW;
}

void loop() {
  buttonState = digitalRead(buttonPin) == LOW;

  if (buttonState != lastButtonState) {
    if (buttonState) {
      clickCount++;  // Aumenta o contador de cliques

      if (clickCount % 2 == 1) {
        Serial.println("1");
      } else {
        Serial.println("2");
      }
    }
    lastButtonState = buttonState;
  }

  if (Serial.available() > 0) {
    comando = Serial.read();

    if (comando == 'R' && !gravando) {
      gravando = true;
      digitalWrite(ledVerde, HIGH); 
      Serial.println("Iniciando gravação...");
    } 
    else if (comando == 'S' && gravando) {
      gravando = false;
      digitalWrite(ledVerde, LOW); 
      digitalWrite(ledAmareloeq, LOW); 
      digitalWrite(ledVerdeeq, LOW);
      digitalWrite(ledVermelhoeq, LOW); 
      Serial.println("Gravação finalizada.");  
    } 
    else if (comando == 'T') {
      digitalWrite(ledAmareloeq, HIGH);
      digitalWrite(ledVerdeeq, LOW);
      digitalWrite(ledVermelhoeq, LOW);
    } 
    else if (comando == 'U') {
      digitalWrite(ledAmareloeq, HIGH);
      digitalWrite(ledVerdeeq, HIGH);
      digitalWrite(ledVermelhoeq, LOW);
    } 
    else if (comando == 'V') {
      digitalWrite(ledVerdeeq, HIGH);
      digitalWrite(ledAmareloeq, HIGH);
      digitalWrite(ledVermelhoeq, HIGH);
    }
    else if (comando == 'L') {
      digitalWrite(ledAmareloeq, LOW);
      digitalWrite(ledVerdeeq, LOW);
      digitalWrite(ledVermelhoeq, LOW);
    }
  }
}
