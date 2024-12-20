/**
  ******************************************************************************
  * @file    Templates/BootCM4_CM7/CM7/Src/main.c
  * @author  MCD Application Team
  * @brief   Main program body for Cortex-M7.
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2018 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */

/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include <stdio.h>

/** @addtogroup STM32H7xx_HAL_Examples
  * @{
  */

/** @addtogroup Templates
  * @{
  */

/* Private typedef -----------------------------------------------------------*/
/* Private define ------------------------------------------------------------*/
#define HSEM_ID_0 (0U) /* HW semaphore 0*/

#define I2C_TIMING 0x10C0ECFF

#define BMP280_ADDRESS (0x77 << 1)

// Oversampling definitions
#define OSRS_OFF        0x00
#define OSRS_1          0x01
#define OSRS_2          0x02
#define OSRS_4          0x03
#define OSRS_8          0x04
#define OSRS_16         0x05

// MODE Definitions
#define MODE_SLEEP      0x00
#define MODE_FORCED     0x01
#define MODE_NORMAL     0x03

// Standby Time
#define T_SB_0p5        0x00
#define T_SB_62p5       0x01
#define T_SB_125        0x02
#define T_SB_250        0x03
#define T_SB_500        0x04
#define T_SB_1000       0x05
#define T_SB_10         0x06
#define T_SB_20         0x07

// IIR Filter Coefficients
#define IIR_OFF         0x00
#define IIR_2           0x01
#define IIR_4           0x02
#define IIR_8           0x03
#define IIR_16          0x04

// REGISTERS DEFINITIONS
#define ID_REG          0xD0
#define RESET_REG       0xE0
#define CTRL_HUM_REG    0xF2
#define STATUS_REG      0xF3
#define CTRL_MEAS_REG   0xF4
#define CONFIG_REG      0xF5
#define PRESS_MSB_REG   0xF7
#define TEMP_MSB_REG    0xFA

/* Private macro -------------------------------------------------------------*/
/* Private variables ---------------------------------------------------------*/
/* I2C handler declaration */
I2C_HandleTypeDef I2cHandle;

uint8_t chipID;

uint16_t dig_T1, dig_P1;
int16_t dig_T2, dig_T3, dig_P2, dig_P3, dig_P4, dig_P5, dig_P6, dig_P7, dig_P8, dig_P9;

uint8_t trimdata[32];

uint8_t datatowrite = 0;

uint8_t osrs_t;
uint8_t mode;
uint8_t t_sb;
uint8_t filter;

uint8_t RawData[3];

int32_t tRaw;
float Temperature, Pressure;

/* Private function prototypes -----------------------------------------------*/
static void MPU_Config(void);
static void CPU_CACHE_Enable(void);
static void SystemClock_Config(void);
static void Error_Handler(void);

int32_t BMP280_compensate_T_int32(int32_t adc_T);
uint32_t bmp280_compensate_P_int64(int32_t adc_P);
//uint32_t BMP280_compensate_P_int64(int32_t adc_P);

/* Private functions ---------------------------------------------------------*/
int __io_putchar(int ch)
{
  // Write character to ITM ch.0
  ITM_SendChar(ch);
  return(ch);
}

/**
  * @brief  Main program
  * @param  None
  * @retval None
  */
int main(void)
{
  int32_t timeout;

  /* System Init, System clock, voltage scaling and L1-Cache configuration are done by CPU1 (Cortex-M7)
     in the meantime Domain D2 is put in STOP mode(Cortex-M4 in deep-sleep)
  */

  /* Configure the MPU attributes */
  MPU_Config();

  /* Enable the CPU Cache */
  CPU_CACHE_Enable();

  /* Wait until CPU2 boots and enters in stop mode or timeout*/
  timeout = 0xFFFF;
  while((__HAL_RCC_GET_FLAG(RCC_FLAG_D2CKRDY) != RESET) && (timeout-- > 0));
  if ( timeout < 0 )
  {
    Error_Handler();
  }

 /* STM32H7xx HAL library initialization:
       - Systick timer is configured by default as source of time base, but user
         can eventually implement his proper time base source (a general purpose
         timer for example or other time source), keeping in mind that Time base
         duration should be kept 1ms since PPP_TIMEOUT_VALUEs are defined and
         handled in milliseconds basis.
       - Set NVIC Group Priority to 4
       - Low Level Initialization
     */
  HAL_Init();

  /* Configure the system clock to 400 MHz */
  SystemClock_Config();

  /* When system initialization is finished, Cortex-M7 will release Cortex-M4  by means of
     HSEM notification */

  /*HW semaphore Clock enable*/
  __HAL_RCC_HSEM_CLK_ENABLE();

  /*Take HSEM */
  HAL_HSEM_FastTake(HSEM_ID_0);
  /*Release HSEM in order to notify the CPU2(CM4)*/
  HAL_HSEM_Release(HSEM_ID_0,0);

  /* wait until CPU2 wakes up from stop mode */
  timeout = 0xFFFF;
  while((__HAL_RCC_GET_FLAG(RCC_FLAG_D2CKRDY) == RESET) && (timeout-- > 0));
  if ( timeout < 0 )
  {
    Error_Handler();
  }

  /* Add Cortex-M7 user application code here */

  /*## Configure the I2C peripheral #########################################*/
  I2cHandle.Instance             = I2Cx;
  I2cHandle.Init.Timing          = I2C_TIMING;
  I2cHandle.Init.OwnAddress1     = 0xFF;
  I2cHandle.Init.AddressingMode  = I2C_ADDRESSINGMODE_7BIT;
  I2cHandle.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
  I2cHandle.Init.OwnAddress2     = 0xFF;
  I2cHandle.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
  I2cHandle.Init.NoStretchMode   = I2C_NOSTRETCH_DISABLE;

  if(HAL_I2C_Init(&I2cHandle) != HAL_OK)
  {
    /* Initialization Error */
    Error_Handler();
  }

  /*## Configure BMP280 sensor ##############################################*/

  /* Check the chip ID (Datasheet p.24) */
  HAL_I2C_Mem_Read(&I2cHandle, BMP280_ADDRESS, ID_REG, 1, &chipID, 1, 1000);

  if (chipID != 0x58) Error_Handler();

  /*## Read the Trimming parameters (Datasheet p.21) ########################*/

  // Read NVM from 0x88 to 0x8D - dig_Tx
  HAL_I2C_Mem_Read(&I2cHandle, BMP280_ADDRESS, 0x88, 1, trimdata, 6, 1000);

  dig_T1 = (trimdata[1]<<8) | trimdata[0];
  dig_T2 = (trimdata[3]<<8) | trimdata[2];
  dig_T3 = (trimdata[5]<<8) | trimdata[4];

  HAL_I2C_Mem_Read(&I2cHandle, BMP280_ADDRESS, 0x8E, 1, trimdata, 18, 1000);

    dig_P1 = (trimdata[1]<<8) | trimdata[0];
    dig_P2 = (trimdata[3]<<8) | trimdata[2];
    dig_P3 = (trimdata[5]<<8) | trimdata[4];
    dig_P4 = (trimdata[7]<<8) | trimdata[6];
        dig_P5 = (trimdata[9]<<8) | trimdata[8];
        dig_P6 = (trimdata[11]<<8) | trimdata[10];
        dig_P7 = (trimdata[13]<<8) | trimdata[12];
            dig_P8 = (trimdata[15]<<8) | trimdata[14];
            dig_P9 = (trimdata[17]<<8) | trimdata[16];

  /*## Reset the device (Datasheet p.24) ####################################*/

  datatowrite = 0xB6;  // reset sequence - write 0xB6 to the register 0xE0
  HAL_I2C_Mem_Write(&I2cHandle, BMP280_ADDRESS, RESET_REG, 1, &datatowrite, 1, 1000);

  HAL_Delay(100);

  /*## Set the data acquisition options (Datasheet p.17, p.25) ##############*/

  // Write the temp oversampling along with mode to 0xF4

  osrs_t = OSRS_2;
  mode = MODE_NORMAL;
  datatowrite = (OSRS_16 <<2)|(osrs_t <<5) | mode;
  HAL_I2C_Mem_Write(&I2cHandle, BMP280_ADDRESS, CTRL_MEAS_REG, 1, &datatowrite, 1, 1000);



  HAL_Delay(100);

  /*## Set the Config register (Datasheet p.26) #############################*/

  // Write the standby time and IIR filter coeff to 0xF5
  t_sb = T_SB_0p5;
  filter = IIR_OFF;
  datatowrite = (t_sb <<5) |(filter << 2);
  HAL_I2C_Mem_Write(&I2cHandle, BMP280_ADDRESS, CONFIG_REG, 1, &datatowrite, 1, 1000);

  HAL_Delay(100);

  /* Infinite loop */
  while (1)
  {
    /*## Read raw data (Datasheet p.26) ############################*/

    // Temperature: read the Registers 0xFA to 0xFC
    HAL_I2C_Mem_Read(&I2cHandle, BMP280_ADDRESS, TEMP_MSB_REG, 1, RawData, 3, HAL_MAX_DELAY);

    tRaw = (RawData[0]<<12)|(RawData[1]<<4)|(RawData[2]>>4);

    /*## Calculating data with compensation formula (Datasheet p.22) ####*/

    Temperature = (BMP280_compensate_T_int32 (tRaw)) / 100.0;  // as per datasheet, the temp is x100

    HAL_I2C_Mem_Read(&I2cHandle, BMP280_ADDRESS, PRESS_MSB_REG, 1, RawData, 3, HAL_MAX_DELAY);

    tRaw = (RawData[0]<<12)|(RawData[1]<<4)|(RawData[2]>>4);

    Pressure = (bmp280_compensate_P_int64(tRaw)) / 256.;

    printf("Temperature = %f DegC; Pressure = %f Pa\r\n", Temperature, Pressure);

    HAL_Delay(500);
  }
}

/************* COMPENSATION CALCULATION AS PER DATASHEET (page 25) **************************/

/* Returns temperature in DegC, resolution is 0.01 DegC. Output value of “5123” equals 51.23 DegC.
   t_fine carries fine temperature as global value
*/
int32_t t_fine;
int32_t BMP280_compensate_T_int32(int32_t adc_T)
{
  int32_t var1, var2, T;
  var1 = ((((adc_T>>3) - ((int32_t)dig_T1<<1))) * ((int32_t)dig_T2)) >> 11;
  var2 = (((((adc_T>>4) - ((int32_t)dig_T1)) * ((adc_T>>4) - ((int32_t)dig_T1)))>> 12) *((int32_t)dig_T3)) >> 14;
  t_fine = var1 + var2;
  T = (t_fine * 5 + 128) >> 8;
  return T;
}

uint32_t bmp280_compensate_P_int64(int32_t adc_P)
{
int64_t var1, var2, p;
var1 = ((int64_t)t_fine) - 128000;
var2 = var1 * var1 * (int64_t)dig_P6;
var2 = var2 + ((var1*(int64_t)dig_P5)<<17);
var2 = var2 + (((int64_t)dig_P4)<<35);
var1 = ((var1 * var1 * (int64_t)dig_P3)>>8) + ((var1 * (int64_t)dig_P2)<<12);
var1 = (((((int64_t)1)<<47)+var1))*((int64_t)dig_P1)>>33;
if (var1 == 0)
{
	return 0; // avoid exception caused by division by zero
}
p = 1048576-adc_P;
p = (((p<<31)-var2)*3125)/var1;
var1 = (((int64_t)dig_P9) * (p>>13) * (p>>13)) >> 25;
var2 = (((int64_t)dig_P8) * p) >> 19;
p = ((p + var1 + var2) >> 8) + (((int64_t)dig_P7)<<4);
return (uint32_t)p;
}

/* Returns pressure in Pa as unsigned 32 bit integer in Q24.8 format (24 integer bits and 8 fractional bits).
   Output value of “24674867” represents 24674867/256 = 96386.2 Pa = 963.862 hPa
*/
//uint32_t BMP280_compensate_P_int64(int32_t adc_P)
//{
//  int64_t var1, var2, p;
//  var1 = ((int64_t)t_fine) - 128000;
//  var2 = var1 * var1 * (int64_t)dig_P6;
//  var2 = var2 + ((var1*(int64_t)dig_P5)<<17);
//  var2 = var2 + (((int64_t)dig_P4)<<35);
//  var1 = ((var1 * var1 * (int64_t)dig_P3)>>8) + ((var1 * (int64_t)dig_P2)<<12);
//  var1 = (((((int64_t)1)<<47)+var1))*((int64_t)dig_P1)>>33;
//  if (var1 == 0)
//  {
//    return 0; // avoid exception caused by division by zero
//  }
//  p = 1048576-adc_P;
//  p = (((p<<31)-var2)*3125)/var1;
//  var1 = (((int64_t)dig_P9) * (p>>13) * (p>>13)) >> 25;
//  var2 = (((int64_t)dig_P8) * p) >> 19;
//  p = ((p + var1 + var2) >> 8) + (((int64_t)dig_P7)<<4);
//  return (uint32_t)p;
//}

/*********************************************************************************************************/

/**
  * @brief  System Clock Configuration
  *         The system Clock is configured as follow : 
  *            System Clock source            = PLL (HSE BYPASS)
  *            SYSCLK(Hz)                     = 400000000 (CPU Clock)
  *            HCLK(Hz)                       = 200000000 (Cortex-M4 CPU, Bus matrix Clocks)
  *            AHB Prescaler                  = 2
  *            D1 APB3 Prescaler              = 2 (APB3 Clock  100MHz)
  *            D2 APB1 Prescaler              = 2 (APB1 Clock  100MHz)
  *            D2 APB2 Prescaler              = 2 (APB2 Clock  100MHz)
  *            D3 APB4 Prescaler              = 2 (APB4 Clock  100MHz)
  *            HSE Frequency(Hz)              = 8000000
  *            PLL_M                          = 4
  *            PLL_N                          = 400
  *            PLL_P                          = 2
  *            PLL_Q                          = 4
  *            PLL_R                          = 2
  *            VDD(V)                         = 3.3
  *            Flash Latency(WS)              = 4
  * @param  None
  * @retval None
  */
static void SystemClock_Config(void)
{
  RCC_ClkInitTypeDef RCC_ClkInitStruct;
  RCC_OscInitTypeDef RCC_OscInitStruct;
  HAL_StatusTypeDef ret = HAL_OK;

  /*!< Supply configuration update enable */
  HAL_PWREx_ConfigSupply(PWR_DIRECT_SMPS_SUPPLY);

  /* The voltage scaling allows optimizing the power consumption when the device is
     clocked below the maximum system frequency, to update the voltage scaling value
     regarding system frequency refer to product datasheet.  */
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  while(!__HAL_PWR_GET_FLAG(PWR_FLAG_VOSRDY)) {}

  /* Enable HSE Oscillator and activate PLL with HSE as source */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_BYPASS;
  RCC_OscInitStruct.HSIState = RCC_HSI_OFF;
  RCC_OscInitStruct.CSIState = RCC_CSI_OFF;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;

  RCC_OscInitStruct.PLL.PLLM = 4;
  RCC_OscInitStruct.PLL.PLLN = 400;
  RCC_OscInitStruct.PLL.PLLFRACN = 0;
  RCC_OscInitStruct.PLL.PLLP = 2;
  RCC_OscInitStruct.PLL.PLLR = 2;
  RCC_OscInitStruct.PLL.PLLQ = 4;

  RCC_OscInitStruct.PLL.PLLVCOSEL = RCC_PLL1VCOWIDE;
  RCC_OscInitStruct.PLL.PLLRGE = RCC_PLL1VCIRANGE_1;
  ret = HAL_RCC_OscConfig(&RCC_OscInitStruct);
  if(ret != HAL_OK)
  {
    Error_Handler();
  }

/* Select PLL as system clock source and configure  bus clocks dividers */
  RCC_ClkInitStruct.ClockType = (RCC_CLOCKTYPE_SYSCLK | RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_D1PCLK1 | RCC_CLOCKTYPE_PCLK1 | \
                                 RCC_CLOCKTYPE_PCLK2  | RCC_CLOCKTYPE_D3PCLK1);

  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.SYSCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB3CLKDivider = RCC_APB3_DIV2;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_APB1_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_APB2_DIV2;
  RCC_ClkInitStruct.APB4CLKDivider = RCC_APB4_DIV2;
  ret = HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_4);
  if(ret != HAL_OK)
  {
    Error_Handler();
  }

  /*
  Note : The activation of the I/O Compensation Cell is recommended with communication  interfaces
          (GPIO, SPI, FMC, QSPI ...)  when  operating at  high frequencies(please refer to product datasheet)
          The I/O Compensation Cell activation  procedure requires :
        - The activation of the CSI clock
        - The activation of the SYSCFG clock
        - Enabling the I/O Compensation Cell : setting bit[0] of register SYSCFG_CCCSR

          To do this please uncomment the following code
  */

  /*
  __HAL_RCC_CSI_ENABLE() ;

  __HAL_RCC_SYSCFG_CLK_ENABLE() ;

  HAL_EnableCompensationCell();
  */
}

/**
  * @brief  This function is executed in case of error occurrence.
  * @param  None
  * @retval None
  */
static void Error_Handler(void)
{
  /* User may add here some code to deal with this error */
  while(1)
  {
  }
}

/**
  * @brief  CPU L1-Cache enable.
  * @param  None
  * @retval None
  */
static void CPU_CACHE_Enable(void)
{
  /* Enable I-Cache */
  SCB_EnableICache();

  /* Enable D-Cache */
  SCB_EnableDCache();
}

/**
  * @brief  Configure the MPU attributes
  * @param  None
  * @retval None
  */
static void MPU_Config(void)
{
  MPU_Region_InitTypeDef MPU_InitStruct;

  /* Disable the MPU */
  HAL_MPU_Disable();

  /* Configure the MPU as Strongly ordered for not defined regions */
  MPU_InitStruct.Enable = MPU_REGION_ENABLE;
  MPU_InitStruct.BaseAddress = 0x00;
  MPU_InitStruct.Size = MPU_REGION_SIZE_4GB;
  MPU_InitStruct.AccessPermission = MPU_REGION_NO_ACCESS;
  MPU_InitStruct.IsBufferable = MPU_ACCESS_NOT_BUFFERABLE;
  MPU_InitStruct.IsCacheable = MPU_ACCESS_NOT_CACHEABLE;
  MPU_InitStruct.IsShareable = MPU_ACCESS_SHAREABLE;
  MPU_InitStruct.Number = MPU_REGION_NUMBER0;
  MPU_InitStruct.TypeExtField = MPU_TEX_LEVEL0;
  MPU_InitStruct.SubRegionDisable = 0x87;
  MPU_InitStruct.DisableExec = MPU_INSTRUCTION_ACCESS_DISABLE;

  HAL_MPU_ConfigRegion(&MPU_InitStruct);

  /* Enable the MPU */
  HAL_MPU_Enable(MPU_PRIVILEGED_DEFAULT);
}

#ifdef  USE_FULL_ASSERT

/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */

  /* Infinite loop */
  while (1)
  {
  }
}
#endif

/**
  * @}
  */

/**
  * @}
  */

