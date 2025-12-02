/*
 * music.h
 *
 *  Created on: 1 дек. 2025 г.
 *      Author: user
 */

#ifndef INC_MUSIC_H_
#define INC_MUSIC_H_

#include <stdbool.h>

const float freq0 = 5.4 * 1000;
const float PERIOD_VALUE12 = (uint32_t)(20000000/freq0 - 1);
const float PULSE_SCALE12 =  (uint32_t)(PERIOD_VALUE12/100.);

bool power_on = false;
float pwm = 0.5;

typedef void (*fptr)();

typedef struct {
	uint8_t ascii;
	fptr funcptr;
} Command;

extern __HAL_TIM_SET_COMPARE;
extern printf;

void set_pwm(float new_pwm) {
//	pwm = pwm > 100. ? 100. : pwm;
//	pwm = pwm < 0. ? 0. : pwm;
	__HAL_TIM_SET_COMPARE(&htim12, TIM_CHANNEL_2, PULSE_SCALE12 * pwm);
}

void power_control() {
	if (power_on) {
		printf("go off\r\n");
		set_pwm(0.);
	}
	else {
		printf("go on\r\n");
		set_pwm(100.);
	}
	power_on = !power_on;
}

Command* commands;
int cnt;

Command init_command(uint8_t ascii, fptr funcptr) {
	Command cmd;
	cmd.ascii = ascii;
	cmd.funcptr = funcptr;
	cnt++;
	return cmd;
}

void call_command(uint8_t ascii) {
	printf("call\r\n");
	for (int i = 0; i < cnt; i++) {
		Command* cmd = &commands[i];
		printf("call: %d, ascii: %d\r\n", i, cmd->ascii);
		if (cmd->ascii == ascii) {
			cmd->funcptr();
			printf("ok\r\n");
			return;
		}
	}
}

#endif /* INC_MUSIC_H_ */
