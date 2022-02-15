int light_sensor = A9; // light sensor connected to port A9
int LED_light_sensor = A6; //light sensor connected to port A6. To view when victim is found

void setup () {
    pinMode(light_sensor, INPUT);
    pinMode(LED_light_sensor, OUTPUT);
    Serial.begin(9600);
}

void loop () {

    float light_sensor_input = analogRead (light_sensor); //takes input from light sensor

    /* If the luminance is less than 100 lx, the LED will turn on, and a screen message will be printed. */
    if (light_sensor_input < 100) {
        digitalWrite (LED_light_sensor, HIGH);
        Serial.println("Target has been found");     
        delay(1000); 
    }

    digitalWrite(LED_light_sensor, LOW);
}