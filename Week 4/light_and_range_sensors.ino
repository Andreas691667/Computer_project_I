int light_sensor = A9; // light sensor connected to port A9
int LED_light_sensor = A6; //light sensor connected to port A6. To view when victim is found
int front_range_sensor = A1; //range front_range_sensor connected to port A0
int left_range_sensor = A0; //range left_range_sensor connected to port A1
int right_range_sensor = A2; //range right_range_sensor connected to port A2
int LED_front = A3; //LED connected to port A3
int LED_right = A10; //LED connected to port A10

//input variables
double front_input = 0; 
double left_input = 0; 
double right_input = 0; 
double front_input_cm = 0;
double left_input_cm = 0;
double right_input_cm = 0;
float light_sensor_input = 0;

void setup () {
    
    //circular inputs
    pinMode(front_range_sensor, INPUT); //front_range_sensor declared as an input
    pinMode(left_range_sensor, INPUT); //left_range_sensor declared as an input
    pinMode(right_range_sensor, INPUT); //right_range_ declared as an input
    pinMode(light_sensor, INPUT);

    //circuit outputs
    pinMode(LED_front, OUTPUT); 
    pinMode(LED_right, OUTPUT);
    pinMode(LED_light_sensor, OUTPUT);

    //initialize serial monitor
    Serial.begin(9600);
}

//function to print all distance measurements (in cm)
void print_all() {
  Serial.print("Distance to front: ");
  Serial.println(front_input_cm);
  Serial.print("Distance to left: ");
  Serial.println(left_input_cm);  
  Serial.print("Distance to right: ");
  Serial.println(right_input_cm);
  Serial.println();
}

//function to make three LED's blink when measurement in some interval is seen
void blink_all() {

    int margin = 0;
      
    if (front_input_cm+margin < 30 && front_input_cm+margin > 0) {
        digitalWrite(LED_front,HIGH);
        delay(50);
        digitalWrite(LED_front,LOW);
        delay(50);
    }

    if (left_input_cm+margin < 30 && left_input_cm+margin > 0) {
        TXLED0;
        delay(50);
        TXLED1;
        delay(50);
    }

    if (right_input_cm+margin < 30 && right_input_cm+margin > 0) {
        digitalWrite(LED_right,HIGH);
        delay(50);
        digitalWrite(LED_right,LOW);
        delay(50);
    }
}

void loop () {

    //take input values from all sensors
    light_sensor_input = analogRead (light_sensor); //takes input from light sensor
    front_input = analogRead(front_range_sensor); 
    left_input = analogRead(left_range_sensor);
    right_input = analogRead(right_range_sensor);

    /*
    The sensor uses a scaling factor of 6.4 mV/inch. By dividing the analog input with this scaling factor,
    a measurement in inches is calculated. Afterwards, this is multiplied by 2.54 cm/inch.
    */
    front_input_cm = (front_input/6.4)*2.54;
    left_input_cm = (left_input/6.4)*2.54;
    right_input_cm = (right_input/6.4)*2.54;

    print_all();

    blink_all();  

    //light sensor readings
    if (light_sensor_input <= 40) {
        
        /* If the luminance is less than 30 lx, the LED will turn on, and a screen message will be printed. */
        if (light_sensor_input < 30) {
            digitalWrite (LED_light_sensor, HIGH);
            Serial.println("Target has been found");     
            delay(1000); 
        }

        /*If the reading is on the borderline of a successful reading, the robot will
        turn back a bit and then forward to make a second reading. */
        else if (light_sensor_input <= 30 && light_sensor_input <= 40) {
            Serial.println("Robot is turning back for 5 seconds");
            Serial.println("Robot is turning forth until target");

            if (light_sensor_input < 30) {
                digitalWrite (LED_light_sensor, HIGH);
                Serial.println("Target has been found");     
                delay(1000); 
            }
        }
    }

    TXLED1; //green LED turned off by default  
    RXLED1; //yellow LED turned off by default
    digitalWrite(LED_light_sensor, LOW);
}