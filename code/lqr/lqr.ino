/******************************************************************/

#include "my_encoders.h"
#include "Motor.h"

/******************************************************************/

Motor Motor;

void setup()
{
  Serial.begin( 1000000 );
  while ( !Serial ) {};
  Serial.setTimeout(100);
  Motor.Motor_init();
  Encoder_init( &(Motor.left_angle), &(Motor.right_angle) );
}

float k1 = 960;
float k2 = 28.5;
float ts = 0.002;
float MAX_ANGLE = 0.6;

/******************************************************************/

bool VERBOSE = false;
unsigned long start_micros = -1;
unsigned long timestep_micros = 2000;
unsigned long next_timestep_micros = -1;

void loop()
{
  Encoder_init( &(Motor.left_angle), &(Motor.right_angle) );
  start_micros = micros();
  next_timestep_micros = 0;
  float previous_angle_radians = 0;
  float desired_angle_radians = 0;
  Serial.println("READY");
  while (true) {
    if ( Serial.available() > 0 ) {
      String s = Serial.readStringUntil('\n');
      char *cmd = s.c_str();
      if (VERBOSE) {
        Serial.print("Received: ");
        Serial.println(cmd);
      }
      if (cmd[0] == 'v') {
        VERBOSE = !VERBOSE;
      } else {
        desired_angle_radians = atof(cmd);
        if (desired_angle_radians > MAX_ANGLE) {
          desired_angle_radians = MAX_ANGLE;
        }
        if (desired_angle_radians < -MAX_ANGLE) {
          desired_angle_radians = -MAX_ANGLE;
        }
      }
    }

    unsigned long current_micros = micros();
    unsigned long elapsed_micros = current_micros - start_micros;
    unsigned long elapsed_millis = elapsed_micros / 1000;

    // Timekeeping
    if (elapsed_micros < next_timestep_micros) {
      continue;
    }
    next_timestep_micros += timestep_micros;

    // Read encoders
    Read_encoders( &(Motor.left_angle), &(Motor.right_angle) );

    // Compute angle and velocity
    float current_angle_encoder = ((float)Motor.left_angle + (float)Motor.right_angle) / 2.0;
    float current_angle_radians = current_angle_encoder / 780.0 * PI;
    float current_velocity_radians = (current_angle_radians - previous_angle_radians) / ts;
    previous_angle_radians = current_angle_radians;

    // Do LQR
    float desired_velocity = 0;

    float current_error_radians = desired_angle_radians - current_angle_radians;
    float current_velocity_error = desired_velocity - current_velocity_radians;

    long command = k1 * current_error_radians + k2 * current_velocity_error;

    // Safety
    if (command > 255) {
      command = 255;
    }
    if (command < -255) {
      command = -255;
    }

    // Logging
    if (VERBOSE) {
      Serial.print("elapse:");
      Serial.println(elapsed_micros);
      Serial.print("angle:");
      Serial.println(current_angle_radians);
      Serial.print("vel:");
      Serial.println(current_velocity_radians);
      Serial.print("des angle:");
      Serial.println(desired_angle_radians);
      Serial.print("des vel:");
      Serial.println(desired_velocity);
      Serial.print("cmd:");
      Serial.println(command);
      Serial.println("-----");
    }

    Motor.Left_command(command);
    Motor.Right_command(command);
  }

  Motor.Stop();
}

/******************************************************************/
