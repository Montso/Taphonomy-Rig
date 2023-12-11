#define HX711_DOUT D3
#define HX711_CLK D2


const uint16_t maximum_lifting_time = 4000;
const uint16_t minimum_lifting_time = 2500;
const uint16_t pause_after_lift = 10000;
const uint8_t weights_array_size = 10;
const uint8_t std_dev_threshold = 4;
const float upper_weight_window = 0.75;
const uint16_t number_of_samples_in_average = 200;
const uint32_t led_indication_time = 180000;
const float cal_factor_battery = 99.78;

HX711ADC scale;

const float cal_factor = 13966;
uint32_t scale_offset = 0;

uint8_t error_indicator = 0;
uint8_t flag_tx_currently = 0;
uint32_t transmission_attempt = 1;
int last_status_code;

uint8_t tramsmit_packet_size = 30;
uint8_t maximum_packet_size = 40;
uint8_t current_packet_size = 0;                    //probably unimplemented in this design as I am copying and pasting to save time.

struct data_template{ 
String      sensor_id;                              //Sensor ID
String      data_packet;                            //DataPacket
uint32_t    time_stamp;                             //Timestamp associated
uint8_t     alarm_state;
};

struct configuration{
uint16_t    battery_voltage; //   battVoltage     - Battery Voltage on the Single Cell LiIon battery (mV)
uint8_t     state_of_charge; //   stateIn         - The SoC of the battery from the onboard fuel gauge
int8_t      rssi;            //   rssiIn          - The Receiver Signal Strength Indicator for the Cellular module
};

//   number_of_send_attempts = SAMPLE_INT - number_of_samples - Provides information indicating what sample achieved a successful transmission. Useful with LastStatus

configuration conf;
data_template data[ARRAY_SIZE];  //data Array for storing data
uint8_t data_index_start = 0;
uint8_t data_index_stop = 0;

// Headers currently need to be set at init, useful for API keys etc.
http_header_t headers[] = {
    { "Content-Type", "application/json" },
    { NULL, NULL } // NOTE: Always terminate headers will NULL
};

http_request_t request;
http_response_t response;

STARTUP(cellular_credentials_set(api, "", "", NULL));        //Necessary for 3rd party SIMs on restart
//TX END-------------

uint8_t lift_count = 0;
uint8_t first_lift_flag = 1;                        //Flag for whether there has been a previous weigh event
uint16_t buzzer_beep_length = 3000;                  //Measured in milliseconds
uint8_t buzzer_error_code = 0;                      //Number of Beeps of Errors
uint16_t dumb_lifting_time = minimum_lifting_time;  //Measured in milliseconds
float last_weight = 0;                              //last measured weight
float weights[weights_array_size] = {0,0,0,0,0,0,0,0,0,0};
uint8_t weights_index = 0;
uint8_t drift_log_flag = 1;

uint32_t start_time_current_weigh = 0;                      //Time when the first dumb weigh in began. (Used for Serial Printouts)
uint32_t initial_lift_delay = 44400;                        //delay from plug in to first automated logged lift (2nd lift) (Start at 11h40 expected lift of 12h00)
uint32_t last_weigh_event_time = 0;                         //Last time a weigh event occured
uint8_t drift_events_per_weighing = 24;
uint32_t weigh_interval = 86400;			                  // (5min:300) (30Min:1800) (24Hours:86400)
uint8_t nocturnal_delay_flag = 1;

uint32_t heartbeat_last_sample_time = Time.now();

void loop() 
{
  //Lift and write to SD
  current_time = Time.now();
  uint8_t tx = error_indicator;
  Serial.println(current_time-last_weigh_event_time);
  Serial.println((weigh_interval/drift_events_per_weighing * drift_log_flag));
  uint8_t trigger_lift_flag = digitalRead(TRIGGER_LIFT);
  if((current_time - last_weigh_event_time) > (weigh_interval/drift_events_per_weighing * drift_log_flag))
  {
      Serial.print("About to do a drift event waiting ");
      myFile = sd.open("/pig_logs/log.txt", FILE_WRITE);
      scale.power_up();
      delay(500);
      current_time = Time.now();
      //Pulled from Penguin
      
      data[data_index_stop].sensor_id = "drift";
      data[data_index_stop].data_packet = "{\"drift\":"+String(scale.get_units(10),3)+",\"battV\":"+String(analogRead(BATTERY_VOLTAGE)/cal_factor_battery,3)+"}";
      data[data_index_stop].time_stamp = current_time;
      data[data_index_stop].alarm_state = 0;

      Serial.print("Packet: ");
      Serial.println(data_index_stop - data_index_start);
      Serial.println("{\""+data[data_index_stop].sensor_id+"\": "+data[data_index_stop].data_packet+", \"ts\": "+String(data[data_index_stop].time_stamp)+", \"alarm\": "+String(data[data_index_stop].alarm_state)+"}");
      if(increment_if_possible(&data_index_stop,ARRAY_SIZE)==0)
      {
        data_index_stop = 0;
      }
      // Penguin Theft end
      
        for (uint16_t i = 0;i<number_of_samples_in_average;i++)
        {
          last_weight = scale.get_units(1);              
          Serial.print("Drift: ");
          Serial.println(last_weight);
          myFile.print("Drift Event: ");
          myFile.print(drift_log_flag);
          myFile.print("\treading: ");
          myFile.print(last_weight);
          myFile.print("\tTime:\t");
          myFile.println(millis());
        }
        myFile.print("Battery Voltage ");
        myFile.print(analogRead(BATTERY_VOLTAGE)/cal_factor_battery,2);
        myFile.print("\tEvent True Time: ");
        myFile.println(Time.now());
        myFile.close();
        scale.power_down();
        drift_log_flag++;
        delay(500);
        digitalWrite(LED,LOW);
  }
  
  //LIFT TIME
  if(((current_time - last_weigh_event_time) > weigh_interval) || (trigger_lift_flag==0)) //Is it time to lift?
  {
    if(trigger_lift_flag==0)
    {
		Serial.println("Triggered Lift Event");    
    }
    else
    {
		drift_log_flag = 1;
		last_weigh_event_time = current_time;
		Serial.println("Automated Lift Event");
    }
    lift_count++;
    start_time_current_weigh = millis();
    uint8_t still_lifting = 1;
    scale.power_up();
    digitalWrite(RAISE_WINCH, LOW);                                                //Set lifting to 1
    while((start_time_current_weigh + maximum_lifting_time > millis()) && (still_lifting == 1))
    {
      weights[weights_index] = scale.get_units(1);
      Serial.print(weights[weights_index]);
      Serial.print("\t");
      Serial.print("Lifting...\t");

      //Time to check
      if(weights[weights_index]>upper_weight_window*last_weight)
      {//Ensure we not in the beginning
        float mean = 0;
        for (int i = 0;i<weights_array_size;i++)
        {
          mean += weights[i];
        }
        Serial.print("Mean: ");
        mean = mean/weights_array_size;
        Serial.print(mean);
        float std_dev_pow2 = 0;
        for (int i = 0;i<weights_array_size;i++)
        {
          std_dev_pow2 = (weights[i] - mean)*(weights[i] - mean);
        }
        Serial.print("\tSTDDev^2: ");
        Serial.println(std_dev_pow2);
        if(std_dev_pow2 < std_dev_threshold)
        {
          still_lifting = 0;
          if(millis() - start_time_current_weigh < minimum_lifting_time)
          {
            uint8_t max_runs = 0;
            while((millis() - start_time_current_weigh < minimum_lifting_time)&&(max_runs<30))
            {
              Serial.println("lifting to greater than minimum_lift_time");
              max_runs++;
              delay(50);
            }
          }
        }
      }
      else
      {
        Serial.println();
      }
      
      weights_index = (weights_index+1)%weights_array_size;
      delay(20);
    }
    uint16_t lifting_duration = millis() - start_time_current_weigh;
    digitalWrite(RAISE_WINCH, HIGH);                                                //Set Lifting to 0
    for (int i = 0; i<weights_array_size;i++)
    {
      Serial.print("weights[");
      Serial.print(i);
      Serial.print("]:\t");
      Serial.println(weights[i]);
    }
    
    Serial.print("Lifting Complete\t");
    if(still_lifting)                               //Stopped because of timeout and not happy weigh_event
    {
      Serial.print("Lifting Timeout exceeded\t");
    }
    else
    {
      Serial.print("Happy weigh_event\t");
    }
    Serial.print("Lift Duration: ");
    Serial.println(lifting_duration);
    Serial.println("Pause before weighing rig");

    delay(pause_after_lift);                                    //Wait a bit
    myFile = sd.open("/pig_logs/log.txt", FILE_WRITE);
    for (uint16_t i = 0;i<number_of_samples_in_average;i++)
    {
      last_weight = scale.get_units(1);              //Average over 10 samples - I suspect this is 1 second
      Serial.print("Estimated Weight: ");
      Serial.println(last_weight);
      myFile.print("Triggered Weigh_in event: ");
      myFile.print(lift_count);
      myFile.print("\tWeight: ");
      myFile.print(last_weight);
      myFile.print("\tTime:\t");
      myFile.println(millis());
    }
    myFile.print("Event True Time: ");
    myFile.println(Time.now());
    myFile.close();
    
    //Penguin Theft AGAIN
    
	long rawRead = scale.read()-scale_offset;
    float value = (rawRead)/cal_factor;
	
	if(trigger_lift_flag == 0)
	{
        data[data_index_stop].sensor_id = "button_weight";
	}
	else
	{
	    data[data_index_stop].sensor_id = "auto_weight";
	}
    data[data_index_stop].data_packet = String(value,3);
    data[data_index_stop].time_stamp = Time.now();
    data[data_index_stop].alarm_state = 0;

    Serial.print("Packet: ");
    Serial.println(data_index_stop - data_index_start);
    Serial.println("{\""+data[data_index_stop].sensor_id+"\": "+data[data_index_stop].data_packet+", \"ts\": "+String(data[data_index_stop].time_stamp)+", \"alarm\": "+String(data[data_index_stop].alarm_state)+"}");
    myFile.println("{\""+data[data_index_stop].sensor_id+"\": "+data[data_index_stop].data_packet+", \"ts\": "+String(data[data_index_stop].time_stamp)+", \"alarm\": "+String(data[data_index_stop].alarm_state)+"}");
    
    if(increment_if_possible(&data_index_stop,ARRAY_SIZE)==0)
    {
        data_index_stop = 0;
    }
    tx = 1;
    
    //Penguin Theft end
    
    //----------------------------------------------------AUTOMATED LOWERING----------------------------------------------------------
    Serial.println("Lowering");
    start_time_current_weigh = millis();
    digitalWrite(LOWER_WINCH, LOW);
    still_lifting = 1;
    while((start_time_current_weigh + lifting_duration > millis())&& (still_lifting == 1))
    {
      weights[weights_index] = scale.get_units(1);
      Serial.print(weights[weights_index]);
      Serial.print("\t");
      Serial.print("Moving...\t");

      //Time to check
      if(weights[weights_index]<(1-upper_weight_window)*last_weight)
      {//Ensure we not in the beginning
        float mean = 0;
        for (int i = 0;i<weights_array_size;i++)
        {
          mean += weights[i];
        }
        Serial.print("Mean: ");
        mean = mean/weights_array_size;
        Serial.print(mean);
        float std_dev_pow2 = 0;
        for (int i = 0;i<weights_array_size;i++)
        {
          std_dev_pow2 = (weights[i] - mean)*(weights[i] - mean);
        }
        Serial.print("\tSTDDev^2: ");
        Serial.println(std_dev_pow2);
        if(std_dev_pow2 < std_dev_threshold)
        {
          still_lifting = 0;
        }
      }
      else
      {
        Serial.println();
      }
      
      weights_index = (weights_index+1)%weights_array_size;
      delay(20);
    }
    digitalWrite(LOWER_WINCH,HIGH);
    
    scale.power_down();
  }
  else
  {
    Serial.print("Well, this is an awkward pause\tNext lift: ");
    Serial.print(weigh_interval);
    Serial.print("\tCurrent Time: ");
    Serial.println((current_time - last_weigh_event_time));
  }
  delay(1000);
}