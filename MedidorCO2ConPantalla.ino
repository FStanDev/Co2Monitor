// include the library code:
#include <LiquidCrystal.h>
#include <Adafruit_SCD30.h>

Adafruit_SCD30  scd30;

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);


void setup() {
  // set up the number of columns and rows on the LCD
  lcd.begin(16, 2);



  // Print a message to the LCD.
  lcd.print("Starting");
  // set the cursor to column 0, line 1
  // line 1 is the second row, since counting begins with 0
  lcd.setCursor(0, 1);
  // print to the second line
  lcd.print(".");
  Serial.begin(9600);
  while (!Serial) delay(10);

  if (!scd30.begin()) {
    Serial.println("Failed to find SCD30 chip");
    while (1) { delay(10); }
  }
  lcd.print("..");
  Serial.println("SCD30 Found!");

  Serial.print("Measurement Interval: "); 
  Serial.print(scd30.getMeasurementInterval()); 
  Serial.println(" seconds");

  Serial.print("Self Calibration = "); Serial.println(scd30.selfCalibrationEnabled());
  Serial.print("Cal Reference = "); Serial.println(scd30.getForcedCalibrationReference());
  Serial.print("Altitude Offset = "); Serial.println(scd30.getAltitudeOffset());
  Serial.print("Temperature Offset = "); Serial.println(scd30.getTemperatureOffset());
  lcd.print("...");
}

void loop() {
  if (scd30.dataReady()){
    Serial.println("Data available!");

    if (!scd30.read()){ Serial.println("Error reading sensor data"); return; }

    Serial.print("Temperature: ");
    Serial.print(scd30.temperature);
    Serial.println(" degrees C");
    
    Serial.print("Relative Humidity: ");
    Serial.print(scd30.relative_humidity);
    Serial.println(" %");
    
    Serial.print("CO2: ");
    Serial.print(scd30.CO2, 3);
    Serial.println(" ppm");
    Serial.println("");

    // set the cursor to column 0, line 1
    // line 1 is the second row, since counting begins with 0
    lcd.setCursor(0, 0);
    // print to the second line
    lcd.print("CO2: " + String(scd30.CO2,2) + " ppm");
    lcd.setCursor(0, 1);
    lcd.print(String(scd30.temperature,2) + " C  " + String(scd30.relative_humidity,2) + "%");

  } else {
    Serial.println("No data");
  }

  delay(100);

}
