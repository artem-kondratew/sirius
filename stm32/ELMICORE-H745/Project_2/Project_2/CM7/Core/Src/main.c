/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2025 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "cmsis_os.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include <stdio.h>
#include <stdbool.h>
#include <stm32h7xx_hal_tim.h>
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

#ifndef HSEM_ID_0
#define HSEM_ID_0 (0U) /* HW semaphore 0*/
#endif
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
ADC_HandleTypeDef hadc1;

TIM_HandleTypeDef htim12;

UART_HandleTypeDef huart3;

/* Definitions for defaultTask */
osThreadId_t defaultTaskHandle;
const osThreadAttr_t defaultTask_attributes = {
  .name = "defaultTask",
  .stack_size = 128 * 4,
  .priority = (osPriority_t) osPriorityNormal,
};
/* Definitions for THREAD1 */
osThreadId_t THREAD1Handle;
const osThreadAttr_t THREAD1_attributes = {
  .name = "THREAD1",
  .stack_size = 128 * 4,
  .priority = (osPriority_t) osPriorityNormal,
};
/* Definitions for THREAD2 */
osThreadId_t THREAD2Handle;
const osThreadAttr_t THREAD2_attributes = {
  .name = "THREAD2",
  .stack_size = 128 * 4,
  .priority = (osPriority_t) osPriorityNormal,
};
/* Definitions for Mutex */
osMutexId_t MutexHandle;
const osMutexAttr_t Mutex_attributes = {
  .name = "Mutex"
};
/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
void PeriphCommonClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_USART3_UART_Init(void);
static void MX_TIM12_Init(void);
static void MX_ADC1_Init(void);
void StartDefaultTask(void *argument);
void proc_terminal_input(void *argument);
void read_from_ADC(void *argument);

/* USER CODE BEGIN PFP */
#ifdef __GNUC__
/* With GCC/RAISONANCE, small printf (option LD Linker->Libraries->Small printf
   set to 'Yes') calls __io_putchar() */
#define PUTCHAR_PROTOTYPE int __io_putchar(int ch)
#else
#define PUTCHAR_PROTOTYPE int fputc(int ch, FILE *f)
#endif /* __GNUC__ */
/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
__IO uint16_t uhADCxConvertedValue = 0;

float freq;
float PERIOD_VALUE12;
float PULSE_SCALE12;
float pwm;
float* octaves;
int note_idx;
int octaves_idx;

#define SHORT_OCTAVE 0
#define FIRST_OCTAVE 1
#define SECOND_OCTAVE 2
#define THIRD_OCTAVE 3

#define LA  0
#define SI  1
#define DO  2
#define RE  3
#define MI  4
#define FA  5
#define SOL 6

bool power_on = false;

typedef void (*fptr)();

const float short_octaves[] = {220.00, 246.96, 130.82, 147.83, 164.81, 174.62, 196.00};
const float first_octaves[] = {440.00, 493.88, 261.63, 293.66, 329.63, 349.23, 392.00};
const float second_octaves[] = {880.00, 987.75, 523.25, 587.32, 659.26, 698.46, 784.00};
const float third_octaves[] = {1720.00, 1975.50, 1046.50, 1174.60, 1318.50, 1396.90, 1568.00};

//const float short_octaves[] = {2830.53, 2869.99, 2700.00, 2724.90, 2749.75, 2764.11, 2795.40};
//const float first_octaves[] = {3152.54, 3231.40, 2891.46, 2938.34, 2990.99, 3019.68, 3082.28};
//const float second_octaves[] = {3796.55, 3954.26, 3274.39, 3368.16, 3473.46, 3530.84, 3656.04};
//const float third_octaves[] = {5026.03, 5400.00, 4040.25, 4227.75, 4438.37, 4553.12, 4803.56};

const float* octaves_list[] = {short_octaves, first_octaves, second_octaves, third_octaves};

typedef struct {
	uint8_t ascii;
	fptr funcptr;
} Command;

Command* commands;
int cnt;

void set_pwm(float new_pwm) {
	osMutexAcquire(MutexHandle, osWaitForever);
	pwm = new_pwm;
	__HAL_TIM_SET_COMPARE(&htim12, TIM_CHANNEL_2, PULSE_SCALE12 * new_pwm);
	osMutexRelease(MutexHandle);
}

void set_frequency(float frequency) {
	freq = frequency;
	PERIOD_VALUE12 = (uint32_t)(20000000/freq - 1);
	PULSE_SCALE12 =  (uint32_t)(PERIOD_VALUE12/100.);
	__HAL_TIM_SET_AUTORELOAD(&htim12, PERIOD_VALUE12);
	set_pwm(pwm);
}

void set_note(int note) {
	float frequency = octaves[note] + 400;
	set_frequency(frequency);
}

void set_short_octave() {
	octaves = (float*)octaves_list[SHORT_OCTAVE];
	octaves_idx = SHORT_OCTAVE;
	printf("setting SHORT octave\r\n");
	set_note(note_idx);
}

void set_first_octave() {
	octaves = (float*)octaves_list[FIRST_OCTAVE];
	octaves_idx = FIRST_OCTAVE;
	printf("setting FIRST octave\r\n");
	set_note(note_idx);
}

void set_second_octave() {
	octaves = (float*)octaves_list[SECOND_OCTAVE];
	octaves_idx = SECOND_OCTAVE;
	printf("setting SECOND octave\r\n");
	set_note(note_idx);
}

void set_third_octave() {
	octaves = (float*)octaves_list[THIRD_OCTAVE];
	octaves_idx = THIRD_OCTAVE;
	printf("setting THIRD octave\r\n");
	set_note(note_idx);
}

void print_arrows() {
	uint8_t arrows[] = {62, 62, 62, 32};
	HAL_UART_Transmit(&huart3, arrows, 4, HAL_MAX_DELAY);
}

void print_menu() {
	printf("' ' - power on/off, 'a' - La, 'b' - Si, 'c' - Do, 'd' - Re, 'e' - Mi, 'f' - Fa, 'g' - Sol\r\n");
	printf("'0' - short octave, '1' - 1-st octave, '2' - 2-nd octave, '3' - 3-rd octave\r\n");
	printf("'m' - call menu\r\n");
}

void print_character(uint8_t ch) {
	HAL_UART_Transmit(&huart3, &ch, 1, HAL_MAX_DELAY);
	printf("\r\n");
}

void poweroff(bool use_print) {
	if (use_print) {
		printf("go off\r\n");
	}
	set_pwm(0);
}

void poweron() {
	printf("go on\r\n");
	set_pwm(pwm);
}

void power_control() {
	if (power_on) {
		poweroff(true);
	}
	else {
		poweron();
	}
	power_on = !power_on;
}

void set_la() {
	set_note(LA);
	note_idx = LA;
	printf("setting LA note\r\n");
}

void set_si() {
	set_note(SI);
	note_idx = SI;
	printf("setting SI note\r\n");
}

void set_do() {
	set_note(DO);
	note_idx = DO;
	printf("setting DO note\r\n");
}

void set_re() {
	set_note(RE);
	note_idx = RE;
	printf("setting RE note\r\n");
}

void set_mi() {
	set_note(MI);
	note_idx = MI;
	printf("setting MI note\r\n");
}

void set_fa() {
	set_note(FA);
	note_idx = FA;
	printf("setting FA note\r\n");
}

void set_sol() {
	set_note(SOL);
	note_idx = SOL;
	printf("setting SOL note\r\n");
}

Command init_command(uint8_t ascii, fptr funcptr) {
	Command cmd;
	cmd.ascii = ascii;
	cmd.funcptr = funcptr;
	cnt++;
	return cmd;
}

void call_command(uint8_t ascii) {
	for (int i = 0; i < cnt; i++) {
		Command* cmd = &commands[i];
		if (cmd->ascii == ascii) {
			cmd->funcptr();
			return;
		}
	}
	printf("Wrong command!\r\n");
}

void set_init_octave() {
	octaves = (float*)octaves_list[THIRD_OCTAVE];
}

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */
/* USER CODE BEGIN Boot_Mode_Sequence_0 */
  int32_t timeout;
/* USER CODE END Boot_Mode_Sequence_0 */

/* USER CODE BEGIN Boot_Mode_Sequence_1 */
  /* Wait until CPU2 boots and enters in stop mode or timeout*/
  timeout = 0xFFFF;
  while((__HAL_RCC_GET_FLAG(RCC_FLAG_D2CKRDY) != RESET) && (timeout-- > 0));
  if ( timeout < 0 )
  {
  Error_Handler();
  }
/* USER CODE END Boot_Mode_Sequence_1 */
  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

/* Configure the peripherals common clocks */
  PeriphCommonClock_Config();
/* USER CODE BEGIN Boot_Mode_Sequence_2 */
/* When system initialization is finished, Cortex-M7 will release Cortex-M4 by means of
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
/* USER CODE END Boot_Mode_Sequence_2 */

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_USART3_UART_Init();
  MX_TIM12_Init();
  MX_ADC1_Init();
  /* USER CODE BEGIN 2 */
  if (HAL_TIM_PWM_Start(&htim12, TIM_CHANNEL_2) != HAL_OK)
  {
    /* PWM generation Error */
    Error_Handler();
  }

  if (HAL_ADCEx_Calibration_Start(&hadc1, ADC_CALIB_OFFSET_LINEARITY, ADC_SINGLE_ENDED) != HAL_OK)
  {
	/* Calibration Error */
	Error_Handler();
  }

  poweroff(false);
  set_init_octave();
  set_note(LA);

  Command powermode = init_command(32, &power_control);           // " "
  Command la_cmd = init_command(97, &set_la);                     // "a"
  Command si_cmd = init_command(98, &set_si);                     // "b"
  Command do_cmd = init_command(99, &set_do);                     // "c"
  Command re_cmd = init_command(100, &set_re);                    // "d"
  Command mi_cmd = init_command(101, &set_mi);                    // "e"
  Command fa_cmd = init_command(102, &set_fa);                    // "f"
  Command sol_cmd = init_command(103, &set_sol);                  // "g"
  Command short_oct_cmd = init_command(48, &set_short_octave);    // "0"
  Command first_oct_cmd = init_command(49, &set_first_octave);    // "1"
  Command second_oct_cmd = init_command(50, &set_second_octave);  // "2"
  Command third_oct_cmd = init_command(51, &set_third_octave);    // "3"
  Command menu_cmd = init_command(109, &print_menu);              // "m"

  Command tmp[] = {
		  powermode,
		  la_cmd,
		  si_cmd,
		  do_cmd,
		  re_cmd,
		  mi_cmd,
		  fa_cmd,
		  sol_cmd,
		  short_oct_cmd,
		  first_oct_cmd,
		  second_oct_cmd,
		  third_oct_cmd,
		  menu_cmd,
  };
  commands = tmp;

  print_menu();
  print_arrows();

  /* USER CODE END 2 */

  /* Init scheduler */
  osKernelInitialize();
  /* Create the mutex(es) */
  /* creation of Mutex */
  MutexHandle = osMutexNew(&Mutex_attributes);

  /* USER CODE BEGIN RTOS_MUTEX */
  /* add mutexes, ... */
  /* USER CODE END RTOS_MUTEX */

  /* USER CODE BEGIN RTOS_SEMAPHORES */
  /* add semaphores, ... */
  /* USER CODE END RTOS_SEMAPHORES */

  /* USER CODE BEGIN RTOS_TIMERS */
  /* start timers, add new ones, ... */
  /* USER CODE END RTOS_TIMERS */

  /* USER CODE BEGIN RTOS_QUEUES */
  /* add queues, ... */
  /* USER CODE END RTOS_QUEUES */

  /* Create the thread(s) */
  /* creation of defaultTask */
  defaultTaskHandle = osThreadNew(StartDefaultTask, NULL, &defaultTask_attributes);

  /* creation of THREAD1 */
  THREAD1Handle = osThreadNew(proc_terminal_input, NULL, &THREAD1_attributes);

  /* creation of THREAD2 */
  THREAD2Handle = osThreadNew(read_from_ADC, NULL, &THREAD2_attributes);

  /* USER CODE BEGIN RTOS_THREADS */
  /* add threads, ... */
  /* USER CODE END RTOS_THREADS */

  /* USER CODE BEGIN RTOS_EVENTS */
  /* add events, ... */
  /* USER CODE END RTOS_EVENTS */

  /* Start scheduler */
  osKernelStart();

  /* We should never get here as control is now taken by the scheduler */
  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Supply configuration update enable
  */
  HAL_PWREx_ConfigSupply(PWR_DIRECT_SMPS_SUPPLY);

  /** Configure the main internal regulator output voltage
  */
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  while(!__HAL_PWR_GET_FLAG(PWR_FLAG_VOSRDY)) {}

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI|RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_BYPASS;
  RCC_OscInitStruct.HSIState = RCC_HSI_DIV1;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLM = 4;
  RCC_OscInitStruct.PLL.PLLN = 400;
  RCC_OscInitStruct.PLL.PLLP = 2;
  RCC_OscInitStruct.PLL.PLLQ = 4;
  RCC_OscInitStruct.PLL.PLLR = 2;
  RCC_OscInitStruct.PLL.PLLRGE = RCC_PLL1VCIRANGE_1;
  RCC_OscInitStruct.PLL.PLLVCOSEL = RCC_PLL1VCOWIDE;
  RCC_OscInitStruct.PLL.PLLFRACN = 0;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2
                              |RCC_CLOCKTYPE_D3PCLK1|RCC_CLOCKTYPE_D1PCLK1;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.SYSCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB3CLKDivider = RCC_APB3_DIV2;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_APB1_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_APB2_DIV2;
  RCC_ClkInitStruct.APB4CLKDivider = RCC_APB4_DIV2;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief Peripherals Common Clock Configuration
  * @retval None
  */
void PeriphCommonClock_Config(void)
{
  RCC_PeriphCLKInitTypeDef PeriphClkInitStruct = {0};

  /** Initializes the peripherals clock
  */
  PeriphClkInitStruct.PeriphClockSelection = RCC_PERIPHCLK_CKPER;
  PeriphClkInitStruct.CkperClockSelection = RCC_CLKPSOURCE_HSI;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief ADC1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_ADC1_Init(void)
{

  /* USER CODE BEGIN ADC1_Init 0 */

  /* USER CODE END ADC1_Init 0 */

  ADC_MultiModeTypeDef multimode = {0};
  ADC_ChannelConfTypeDef sConfig = {0};

  /* USER CODE BEGIN ADC1_Init 1 */

  /* USER CODE END ADC1_Init 1 */

  /** Common config
  */
  hadc1.Instance = ADC1;
  hadc1.Init.ClockPrescaler = ADC_CLOCK_ASYNC_DIV2;
  hadc1.Init.Resolution = ADC_RESOLUTION_16B;
  hadc1.Init.ScanConvMode = ADC_SCAN_DISABLE;
  hadc1.Init.EOCSelection = ADC_EOC_SINGLE_CONV;
  hadc1.Init.LowPowerAutoWait = DISABLE;
  hadc1.Init.ContinuousConvMode = DISABLE;
  hadc1.Init.NbrOfConversion = 1;
  hadc1.Init.DiscontinuousConvMode = DISABLE;
  hadc1.Init.ExternalTrigConv = ADC_SOFTWARE_START;
  hadc1.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_NONE;
  hadc1.Init.ConversionDataManagement = ADC_CONVERSIONDATA_DR;
  hadc1.Init.Overrun = ADC_OVR_DATA_OVERWRITTEN;
  hadc1.Init.LeftBitShift = ADC_LEFTBITSHIFT_NONE;
  hadc1.Init.OversamplingMode = DISABLE;
  if (HAL_ADC_Init(&hadc1) != HAL_OK)
  {
    Error_Handler();
  }

  /** Configure the ADC multi-mode
  */
  multimode.Mode = ADC_MODE_INDEPENDENT;
  if (HAL_ADCEx_MultiModeConfigChannel(&hadc1, &multimode) != HAL_OK)
  {
    Error_Handler();
  }

  /** Configure Regular Channel
  */
  sConfig.Channel = ADC_CHANNEL_2;
  sConfig.Rank = ADC_REGULAR_RANK_1;
  sConfig.SamplingTime = ADC_SAMPLETIME_1CYCLE_5;
  sConfig.SingleDiff = ADC_SINGLE_ENDED;
  sConfig.OffsetNumber = ADC_OFFSET_NONE;
  sConfig.Offset = 0;
  sConfig.OffsetSignedSaturation = DISABLE;
  if (HAL_ADC_ConfigChannel(&hadc1, &sConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN ADC1_Init 2 */

  /* USER CODE END ADC1_Init 2 */

}

/**
  * @brief TIM12 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM12_Init(void)
{

  /* USER CODE BEGIN TIM12_Init 0 */

  /* USER CODE END TIM12_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_OC_InitTypeDef sConfigOC = {0};

  /* USER CODE BEGIN TIM12_Init 1 */

  /* USER CODE END TIM12_Init 1 */
  htim12.Instance = TIM12;
  htim12.Init.Prescaler = 9;
  htim12.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim12.Init.Period = 1;
  htim12.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim12.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;
  if (HAL_TIM_Base_Init(&htim12) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim12, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_TIM_PWM_Init(&htim12) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigOC.OCMode = TIM_OCMODE_PWM1;
  sConfigOC.Pulse = 0;
  sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
  sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
  if (HAL_TIM_PWM_ConfigChannel(&htim12, &sConfigOC, TIM_CHANNEL_2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM12_Init 2 */

  /* USER CODE END TIM12_Init 2 */
  HAL_TIM_MspPostInit(&htim12);

}

/**
  * @brief USART3 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART3_UART_Init(void)
{

  /* USER CODE BEGIN USART3_Init 0 */

  /* USER CODE END USART3_Init 0 */

  /* USER CODE BEGIN USART3_Init 1 */

  /* USER CODE END USART3_Init 1 */
  huart3.Instance = USART3;
  huart3.Init.BaudRate = 115200;
  huart3.Init.WordLength = UART_WORDLENGTH_8B;
  huart3.Init.StopBits = UART_STOPBITS_1;
  huart3.Init.Parity = UART_PARITY_NONE;
  huart3.Init.Mode = UART_MODE_TX_RX;
  huart3.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart3.Init.OverSampling = UART_OVERSAMPLING_16;
  huart3.Init.OneBitSampling = UART_ONE_BIT_SAMPLE_DISABLE;
  huart3.Init.ClockPrescaler = UART_PRESCALER_DIV1;
  huart3.AdvancedInit.AdvFeatureInit = UART_ADVFEATURE_NO_INIT;
  if (HAL_UART_Init(&huart3) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_UARTEx_SetTxFifoThreshold(&huart3, UART_TXFIFO_THRESHOLD_1_8) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_UARTEx_SetRxFifoThreshold(&huart3, UART_RXFIFO_THRESHOLD_1_8) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_UARTEx_DisableFifoMode(&huart3) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART3_Init 2 */

  /* USER CODE END USART3_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOF_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();
  __HAL_RCC_GPIOD_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_15, GPIO_PIN_RESET);

  /*Configure GPIO pin : PA15 */
  GPIO_InitStruct.Pin = GPIO_PIN_15;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

}

/* USER CODE BEGIN 4 */
/**
  * @brief  Retargets the C library printf function to the USART.
  * @param  None
  * @retval None
  */
PUTCHAR_PROTOTYPE
{
  /* Place your implementation of fputc here */
  /* e.g. write a character to the USARTx and Loop until the end of transmission */
  HAL_UART_Transmit(&huart3, (uint8_t *)&ch, 1, HAL_MAX_DELAY);

  return ch;
}
/* USER CODE END 4 */

/* USER CODE BEGIN Header_StartDefaultTask */
/**
  * @brief  Function implementing the defaultTask thread.
  * @param  argument: Not used
  * @retval None
  */
/* USER CODE END Header_StartDefaultTask */
void StartDefaultTask(void *argument)
{
  /* USER CODE BEGIN 5 */
  /* Infinite loop */
  for(;;)
  {
    osDelay(1);
  }
  /* USER CODE END 5 */
}

/* USER CODE BEGIN Header_proc_terminal_input */
/**
* @brief Function implementing the THREAD1 thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_proc_terminal_input */
void proc_terminal_input(void *argument)
{
  /* USER CODE BEGIN proc_terminal_input */
	uint8_t data;
  /* Infinite loop */
  for(;;)
  {
	  HAL_StatusTypeDef status = HAL_UART_Receive(&huart3, &data, 1, HAL_MAX_DELAY);
	  if (status == HAL_OK) {
//		  printf("data: %d\r\n", data);
		  print_character(data);
		  call_command(data);
		  print_arrows();
	  }
  }
  /* USER CODE END proc_terminal_input */
}

/* USER CODE BEGIN Header_read_from_ADC */
/**
* @brief Function implementing the THREAD2 thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_read_from_ADC */
void read_from_ADC(void *argument)
{
  /* USER CODE BEGIN read_from_ADC */
  /* Infinite loop */
  for(;;)
  {
	  if (HAL_ADC_Start(&hadc1) != HAL_OK)
		{
		  /* Start Conversation Error */
		  Error_Handler();
		}
	  if (HAL_ADC_PollForConversion(&hadc1, 10) != HAL_OK)
	    {
	      /* End Of Conversion flag not set on time */
	      Error_Handler();
	    }
	  else
	    {
	      uhADCxConvertedValue = HAL_ADC_GetValue(&hadc1);

	      if (!power_on) {
	    	  continue;
	      }

	      float max_val;
	      if (octaves_idx == SHORT_OCTAVE || octaves_idx == FIRST_OCTAVE) {
	    	  max_val = 10;
	      }
	      else {
	    	  max_val = 10;
	      }

	      float new_pwm = uhADCxConvertedValue / 65535. * max_val;
		  //new_pwm = new_pwm > 50 ? 50 : new_pwm;
		  set_pwm(new_pwm);
		  //printf("%d %d\r\n", uhADCxConvertedValue, (int)(new_pwm));
	    }
      osDelay(1);
  }
  /* USER CODE END read_from_ADC */
}

/**
  * @brief  Period elapsed callback in non blocking mode
  * @note   This function is called  when TIM4 interrupt took place, inside
  * HAL_TIM_IRQHandler(). It makes a direct call to HAL_IncTick() to increment
  * a global variable "uwTick" used as application time base.
  * @param  htim : TIM handle
  * @retval None
  */
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
  /* USER CODE BEGIN Callback 0 */

  /* USER CODE END Callback 0 */
  if (htim->Instance == TIM4) {
    HAL_IncTick();
  }
  /* USER CODE BEGIN Callback 1 */

  /* USER CODE END Callback 1 */
}

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
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
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
