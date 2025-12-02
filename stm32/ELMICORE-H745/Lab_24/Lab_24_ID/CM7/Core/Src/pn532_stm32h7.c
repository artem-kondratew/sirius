
#include "stm32h7xx_hal.h"
#include "main.h"
#include <stdio.h>
#include "pn532_stm32h7.h"

#define _I2C_ADDRESS                    0x48
#define _I2C_TIMEOUT                    10

extern I2C_HandleTypeDef hi2c4;

/**************************************************************************
 * Reset and Log implements
 **************************************************************************/
int PN532_Reset(void) {

    // Reset pin not connected

    return PN532_STATUS_OK;
}

void PN532_Log(const char* log) {
    printf("%s\r\n", log);
}

void PN532_Init(PN532* pn532) {
    PN532_I2C_Init(pn532);
}
/**************************************************************************
 * End: Reset and Log implements
 **************************************************************************/

/**************************************************************************
 * I2C
 **************************************************************************/
void i2c_read(uint8_t* data, uint16_t count) {
    HAL_I2C_Master_Receive(&hi2c4, _I2C_ADDRESS, data, count, _I2C_TIMEOUT);
}

void i2c_write(uint8_t* data, uint16_t count) {
    HAL_I2C_Master_Transmit(&hi2c4, _I2C_ADDRESS, data, count, _I2C_TIMEOUT);
}

int PN532_I2C_ReadData(uint8_t* data, uint16_t count) {
    uint8_t status[] = {0x00};
    uint8_t frame[count + 1];
    i2c_read(status, sizeof(status));
    if (status[0] != PN532_I2C_READY) {
        return PN532_STATUS_ERROR;
    }
    i2c_read(frame, count + 1);
    for (uint8_t i = 0; i < count; i++) {
        data[i] = frame[i + 1];
    }
    return PN532_STATUS_OK;
}

int PN532_I2C_WriteData(uint8_t *data, uint16_t count) {
    i2c_write(data, count);
    return PN532_STATUS_OK;
}

bool PN532_I2C_WaitReady(uint32_t timeout) {
    uint8_t status[] = {0x00};
    uint32_t tickstart = HAL_GetTick();
    while (HAL_GetTick() - tickstart < timeout) {
        i2c_read(status, sizeof(status));
        if (status[0] == PN532_I2C_READY) {
            return true;
        } else {
            HAL_Delay(5);
        }
    }
    return false;
}

int PN532_I2C_Wakeup(void) {

    // Wakeup pin not connected

    return PN532_STATUS_OK;
}

void PN532_I2C_Init(PN532* pn532) {
    // init the pn532 functions
    pn532->reset =  PN532_Reset;
    pn532->read_data = PN532_I2C_ReadData;
    pn532->write_data = PN532_I2C_WriteData;
    pn532->wait_ready = PN532_I2C_WaitReady;
    pn532->wakeup = PN532_I2C_Wakeup;
    pn532->log = PN532_Log;

    // hardware wakeup
    pn532->wakeup();
}
/**************************************************************************
 * End: I2C
 **************************************************************************/
