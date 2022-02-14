
int front_range_sensor = A0; //range front_range_sensor connected to port A0

double front_input = 0; //variable for storing input values

void setup()
{
  pinMode(front_range_sensor,INPUT); //front_range_sensor declarared as an input
  
  Serial.begin(9600); //This pipes to the serial monitor
  Serial.println("Initialize Serial Monitor");
}


void loop()
{
 
  front_input = analogRead(front_range_sensor); 

  Serial.print(front_input+2);
  Serial.println(" cm");

  int margin = 2;


  if (front_input+margin < 20 && front_input+margin > 0) {
    TXLED0;
    delay(50);
    TXLED1;
    delay(50);
  }

  TXLED1; //LED turned off by default  

}
