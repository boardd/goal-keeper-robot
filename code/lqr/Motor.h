#ifndef _MOTOR_H
#define _MOTOR_H

#define MAX_COMMAND 255

class Motor
{
  public:
          // methods
          void Motor_init();
          void Stop();
          void Forward(int speed);
          void Back(int speed);
          void Left(int speed);
          void Right(int speed);
          void Left_command(int speed);
          void Right_command(int speed);

          // variables
          long left_angle;
          long right_angle;
          
  private:
};

#endif
