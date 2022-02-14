
int front_range_sensor = A0; //range front_range_sensor connected to port A0

int left_range_sensor = A1; //range left_range_sensor connected to port A1

int LED = A2; //LED connected to port A2

// int right_range_sensor =

double front_input = 0; //variable for storing input values
double left_input = 0; //variable for storing input values

void setup()
{
  pinMode(front_range_sensor, INPUT); //front_range_sensor declarared as an input

  pinMode(left_range_sensor, INPUT); //left_range_sensor declarared as an input

  pinMode(LED, OUTPUT); //
    
  Serial.begin(9600); //This pipes to the serial monitor
  Serial.println("Initialize Serial Monitor");
}


void loop()
{
  int margin = 0;
  front_input = analogRead(front_range_sensor); 
  left_input = analogRead(left_range_sensor);


  double front_input_cm = (front_input/6.4)*2.54;
  double left_input_cm = (left_input/6.4)*2.54;

  //Serial.println(front_input_cm);
  //Serial.println(left_input_cm);  
  Serial.println();
  
  if (front_input_cm+margin < 30 && front_input_cm+margin > 0) {
    Serial.println("Robot is going backwards");
    TXLED0;
    delay(50);
    TXLED1;
    delay(50);
    delay(2900);
  }

  if (left_input_cm+margin < 30 && left_input_cm+margin > 0) {
    Serial.println("Robot is going right");
      digitalWrite(LED,HIGH);
    delay(50);
      digitalWrite(LED,LOW);
    delay(50);
    delay(2900);
  }

  TXLED1; //green LED turned off by default  

  RXLED1; //yellow LED turned off by default

}
