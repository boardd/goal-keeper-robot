/******************************************************************/

#include "my_encoders.h"
#include "Motor.h"

/******************************************************************/

#define TARGET 500

/******************************************************************/

Motor Motor;

static bool go = false;  /* motor enable */

/******************************************************************/

void setup()
{
  Serial.begin( 1000000 );
  while( !Serial ){};
  delay( 1000 ); // Delay to make sure above message prints out.
  Motor.Motor_init();
  Serial.println( "Motor.Pin_init done." );
  Serial.println( "If we hang here power cycle the robot. Expect more printout" );
  delay( 1000 ); // Delay to make sure above messages print out.
  Encoder_init( &(Motor.left_angle), &(Motor.right_angle) );
  Serial.println( "Encoder_init done." );
  Serial.println( "Wheels should be off the ground."  );
  Serial.println( "Type g <return> to run test, s <return> to stop."  );
  Serial.println( "Typing window is at the top of the serial monitor window" );
}

/******************************************************************/

// Take user input
void ProcessCommand()
{

  if ( Serial.available() <= 0 )
    return;

  int c = Serial.read();
  switch (c)
    {
      case 'S': case 's':
        Serial.println( "Stop!" );
        go = false;
        break;
      case 'G': case 'g':
      Serial.println( "Go!" );
        go = true;
        break;
      default:
        break;
    }
}

/******************************************************************/

unsigned long start_micros = -1;
unsigned long timestep_micros = 2000;
unsigned long next_timestep_micros = -1;

void loop()
{
  if (!go) {
    start_micros = -1;
    next_timestep_micros = -1;
    Motor.Stop();
    ProcessCommand();
    return;
  }

  if (start_micros == -1) {
    start_micros = micros();
    next_timestep_micros = 0;
  }

  unsigned long current_micros = micros();
  unsigned long elapsed_micros = current_micros - start_micros;
  unsigned long elapsed_millis = elapsed_micros / 1000;

  // Reset
  if (elapsed_millis >= 300) {
    Encoder_init( &(Motor.left_angle), &(Motor.right_angle) );
    go = false;
    Motor.Stop();
    return;
  }

  if (elapsed_micros < next_timestep_micros) {
    return;
  }
  next_timestep_micros += timestep_micros;  

  int command = 0;

  if (elapsed_millis >= 0) {
    command = 0;
  }
  if (elapsed_millis >= 50) {
    command = 255;
  }
  if (elapsed_millis >= 125) {
    command = -200;
  }
  if (elapsed_millis >= 200) {
    command = 50;
  }
  if (elapsed_millis >= 250) {
    command = 0;
  }

  Motor.Left_command( command );
  Motor.Right_command( command );

  Read_encoders( &(Motor.left_angle), &(Motor.right_angle) );

  Serial.print(elapsed_millis);
  Serial.print(",");
  Serial.print(Motor.left_angle);
  Serial.print(",");
  Serial.print(Motor.right_angle);
  Serial.print(",");
  Serial.print(command);
  Serial.println("");
}

/******************************************************************/
