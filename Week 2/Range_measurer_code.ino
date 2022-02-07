
int SENSOR = A0; //range sensor connected to port A0

double range_input = 0; //variable for storing input values

void setup()
{
  pinMode(SENSOR,INPUT); //sensor declarared as an input
  
  Serial.begin(9600); //This pipes to the serial monitor
  Serial.println("Initialize Serial Monitor");
}


void loop()
{
 
  range_input = analogRead(SENSOR); 

  Serial.print(range_input+2);
  Serial.println(" cm");


  if (range_input+2 < 20 && range_input+2 > 0) {
    TXLED0;
    delay(100);
  }

  else if (range_input+2 < 30 && range_input+2 > 25) {
    TXLED0;
    delay(100);
    TXLED1;
    delay(100);
  } 
  
  else if(range_input+2 < 25 && range_input+2 >20) {
    TXLED0;
    delay(333);
    TXLED1;
    delay(333);
  }

  TXLED1; //LED turned off by default  

}
