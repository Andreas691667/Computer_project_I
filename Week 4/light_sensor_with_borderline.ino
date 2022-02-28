int light_sensor = A9; // light sensor connected to port A9
int LED_light_sensor = A6; //light sensor connected to port A6. To view when victim is found

void setup () {
    pinMode(light_sensor, INPUT);
    pinMode(LED_light_sensor, OUTPUT);
    Serial.begin(9600);
}

void loop () {

    float light_sensor_input = analogRead (light_sensor); //takes input from light sensor


    if (light_sensor_input <= 33) {
        
        /* If the luminance is less than 30 lx, the LED will turn on, and a screen message will be printed. */
        if (light_sensor_input < 23) {
            digitalWrite (LED_light_sensor, HIGH);
            Serial.println("Target has been found");     
            delay(1000); 
        }

        /*If the reading is on the borderline of a successful reading, the robot will
        turn back a bit and then forward to make a second reading. */
        else if (light_sensor_input <= 23 && light_sensor_input <= 33) {
            Serial.println("Robot is turning back for 5 seconds");
            Serial.println("Robot is turning forth until target");

            if (light_sensor_input < 23) {
                digitalWrite (LED_light_sensor, HIGH);
                Serial.println("Target has been found");     
                delay(1000); 
            }
        }
    }









    digitalWrite(LED_light_sensor, LOW);
}