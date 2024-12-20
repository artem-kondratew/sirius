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
#include <stdbool.h>

/** @addtogroup STM32H7xx_HAL_Examples
  * @{
  */

/** @addtogroup Templates
  * @{
  */

/* Private typedef -----------------------------------------------------------*/
#define  PERIOD_VALUE  (uint32_t)(10000000/200 - 1)      // ARR Value (Period)
#define  PULSE_SCALE   (uint32_t)(PERIOD_VALUE/100) // Capture Compare Value (Duty Cycle)

/* Private define ------------------------------------------------------------*/
#define HSEM_ID_0 (0U) /* HW semaphore 0*/
/* Private macro -------------------------------------------------------------*/
/* Private variables ---------------------------------------------------------*/
/* Timer handler declaration */
TIM_HandleTypeDef TimHandle, TimHandle12, TimHandle4;

/* Timer Output Compare Configuration Structure declaration */
TIM_OC_InitTypeDef sConfig, BuzConfig;

/* Counter Prescaler value */
uint32_t uwPrescalerValue = 0;
uint32_t uwPrescalerValue12 = 0;

/* Private function prototypes -----------------------------------------------*/
static void MPU_Config(void);
static void CPU_CACHE_Enable(void);
static void SystemClock_Config(void);
static void Error_Handler(void);


/* Private functions ---------------------------------------------------------*/

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
//  __HAL_RCC_GPIOD_CLK_ENABLE();
//

  __HAL_RCC_GPIOB_CLK_ENABLE();

  GPIO_InitTypeDef  gpio_init_structure_led;

    gpio_init_structure_led.Pin   = GPIO_PIN_0;
    gpio_init_structure_led.Mode  = GPIO_MODE_OUTPUT_PP;
    gpio_init_structure_led.Pull  = GPIO_NOPULL;
    gpio_init_structure_led.Speed = GPIO_SPEED_FREQ_VERY_HIGH;

    HAL_GPIO_Init(GPIOB, &gpio_init_structure_led);

    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_RESET);

  /*##-1- Configure the TIM peripheral #######################################*/
  /* -----------------------------------------------------------------------
  TIMx Configuration: generate PWM signal.

    TIM3CLK = 2*PCLK1 (since APB1 prescaler is equal to 2)
    PCLK1 = HCLK/2 =>
    TIM3CLK = HCLK = SystemCoreClock/2 (AHB Clock divider is set to RCC_HCLK_DIV2)

    To get TIM3 counter clock at 10 MHz, the prescaler is computed as follows:
      Prescaler = (TIM3CLK / TIM3 counter clock) - 1
      Prescaler = (HCLK /(10 MHz)) - 1

    To get TIM3 output clock (signal frequency) at 200 Hz, the ARR (period) is computed as follows:
      ARR = (TIM3 counter clock / TIM3 output clock) - 1
          = (10 MHz / 200 Hz) - 1

    To get Duty Cycle at 12.5%, the CCR (pulse) is computed as follows:
      CCR = ARR * 12.5 / 100

  ----------------------------------------------------------------------- */

  /* Compute the prescaler value to have TIMx counter clock equal to 10 MHz */
  uwPrescalerValue = (uint32_t)(HAL_RCC_GetHCLKFreq() / 10000000) - 1;

  TimHandle.Instance = TIMx;

  TimHandle.Init.Prescaler         = uwPrescalerValue;
  TimHandle.Init.Period            = PERIOD_VALUE;
  TimHandle.Init.ClockDivision     = 0;
  TimHandle.Init.CounterMode       = TIM_COUNTERMODE_UP;
  TimHandle.Init.RepetitionCounter = 0;
  if (HAL_TIM_PWM_Init(&TimHandle) != HAL_OK)
  {
    /* Initialization Error */
    Error_Handler();
  }

      float freq0 = 5.4 * 1000;  // Hz
//      float freq1 = freq0 * 2;  // Hz

      uwPrescalerValue12 = (uint32_t)(SystemCoreClock / (2 * 20000000.)) - 1;

    TimHandle12.Instance = TIM12;

    float PERIOD_VALUE12 = (uint32_t)(20000000/freq0 - 1);      // ARR Value (Period)


    TimHandle12.Init.Period            = (uint32_t)PERIOD_VALUE12;
    TimHandle12.Init.Prescaler         = uwPrescalerValue12;
    TimHandle12.Init.ClockDivision     = 0;
    TimHandle12.Init.CounterMode       = TIM_COUNTERMODE_UP;
    TimHandle12.Init.RepetitionCounter = 0;
    if (HAL_TIM_PWM_Init(&TimHandle12) != HAL_OK)
    {
      /* Initialization Error */
      Error_Handler();
    }

    TimHandle4.Instance = TIM2;

    TimHandle4.Init.Period            = 20000000 - 1;
    TimHandle4.Init.Prescaler         = (uint32_t)(SystemCoreClock / (2 * 20000000)) - 1;
    TimHandle4.Init.ClockDivision     = 0;
    TimHandle4.Init.CounterMode       = TIM_COUNTERMODE_UP;
    TimHandle4.Init.RepetitionCounter = 0;
        if (HAL_TIM_Base_Init(&TimHandle4) != HAL_OK)
        {
          /* Initialization Error */
          Error_Handler();
        }

        if (HAL_TIM_Base_Start(&TimHandle4) != HAL_OK)
            {
              /* Starting Error */
              Error_Handler();
            }

  uint32_t pwm = PULSE_SCALE * 25;

  /*##-2- Configure the PWM channels #########################################*/
  sConfig.Pulse        = pwm;
  sConfig.OCMode       = TIM_OCMODE_PWM1;
  sConfig.OCPolarity   = TIM_OCPOLARITY_HIGH;
  sConfig.OCFastMode   = TIM_OCFAST_DISABLE;
  sConfig.OCNPolarity  = TIM_OCNPOLARITY_HIGH;
  sConfig.OCNIdleState = TIM_OCNIDLESTATE_RESET;
  sConfig.OCIdleState  = TIM_OCIDLESTATE_RESET;
  if (HAL_TIM_PWM_ConfigChannel(&TimHandle, &sConfig, TIM_CHANNEL_1) != HAL_OK)
  {
    /* Configuration Error */
    Error_Handler();
  }

float PULSE_SCALE12 =  (uint32_t)(PERIOD_VALUE12/100.); // Capture Compare Value (Duty Cycle)

    BuzConfig.Pulse        = PULSE_SCALE12 * 50;
    BuzConfig.OCMode       = TIM_OCMODE_PWM1;
    BuzConfig.OCPolarity   = TIM_OCPOLARITY_HIGH;
    BuzConfig.OCFastMode   = TIM_OCFAST_DISABLE;
    BuzConfig.OCNPolarity  = TIM_OCNPOLARITY_HIGH;
    BuzConfig.OCNIdleState = TIM_OCNIDLESTATE_RESET;
    BuzConfig.OCIdleState  = TIM_OCIDLESTATE_RESET;
    if (HAL_TIM_PWM_ConfigChannel(&TimHandle12, &BuzConfig, TIM_CHANNEL_2) != HAL_OK)
    {
      /* Configuration Error */
      Error_Handler();
    }

  /*##-3- Start PWM signals generation #######################################*/
  if (HAL_TIM_PWM_Start(&TimHandle, TIM_CHANNEL_1) != HAL_OK)
  {
    /* PWM generation Error */
    Error_Handler();
  }

  if (HAL_TIM_PWM_Start(&TimHandle12, TIM_CHANNEL_2) != HAL_OK)
    {
      /* PWM generation Error */
      Error_Handler();
    }

  /* Infinite loop */
  while (1)
  {
	  pwm = PULSE_SCALE * 25;
	  __HAL_TIM_SET_COMPARE(&TimHandle, TIM_CHANNEL_1, pwm);
	  HAL_Delay(1000);
	  pwm = PULSE_SCALE * 75;
	  __HAL_TIM_SET_COMPARE(&TimHandle, TIM_CHANNEL_1, pwm);
	  HAL_Delay(1000);

//	  while (freq0 < 10800) {
//		  freq0 += (10800 - 5400) /1500;
//		  PERIOD_VALUE12 = (uint32_t)(20000000./freq0 - 1);
//		  PULSE_SCALE12 =  (uint32_t)(PERIOD_VALUE12/100.);
//		  __HAL_TIM_SET_AUTORELOAD(&TimHandle12, (uint32_t)PERIOD_VALUE12);
//		  __HAL_TIM_SET_COMPARE(&TimHandle12, TIM_CHANNEL_2, PULSE_SCALE12 * 50.);
//		  HAL_Delay(1);
//	  }
//
//	  while (freq0 > 5400) {
//	  		  freq0 -= (10800 - 5400) /1500;
//	  		  PERIOD_VALUE12 = (uint32_t)(20000000/freq0 - 1);
//	  		  PULSE_SCALE12 =  (uint32_t)(PERIOD_VALUE12/100);
//	  		  __HAL_TIM_SET_AUTORELOAD(&TimHandle12, (uint32_t)PERIOD_VALUE12);
//	  		  __HAL_TIM_SET_COMPARE(&TimHandle12, TIM_CHANNEL_2, PULSE_SCALE12 * 50);
//	  		HAL_Delay(1);
//	  	  }


//	        if (__HAL_TIM_GET_FLAG(&TimHandle4, TIM_FLAG_UPDATE))
//	        {
//	          __HAL_TIM_CLEAR_FLAG(&TimHandle4, TIM_FLAG_UPDATE);
//	          HAL_GPIO_TogglePin(GPIOB, GPIO_PIN_0);
//	        }


//	  HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_SET);   // Включить светодиод
//	  HAL_Delay(500);                                      // Задержка 500 мс
//	  HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_RESET); // Выключить светодиод
//	  HAL_Delay(500);                                      // Задержка 500 мс

  }
}


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

