/* USER CODE BEGIN Header */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE BEGIN Includes */
#include "spi_ili9341.h"
/* USER CODE END Includes */

/* USER CODE BEGIN PV */
extern uint16_t TFT9341_WIDTH;
extern uint16_t TFT9341_HEIGHT;
/* USER CODE END PV */

/* USER CODE BEGIN PFP */
void LCD_Test_1(void);
void LCD_Test_2(void);
void LCD_Test_3(void);
void LCD_Test_4(void);
void LCD_Test_5(void);
void LCD_Test_6(void);
void LCD_Test_7(void);
void LCD_Test_8(void);
void LCD_Test_9(void);
void LCD_Test_10(void);

uint32_t GetRandomNumber(void);
/* USER CODE END PFP */

/* USER CODE BEGIN 0 */
__STATIC_INLINE void DelayMicro(uint32_t __IO micros)
{
  micros *= (SystemCoreClock/1000000);
  while (micros--);
}
/* USER CODE END 0 */
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */
/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */
/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

RNG_HandleTypeDef hrng;

SPI_HandleTypeDef hspi2;

/* USER CODE BEGIN PV */
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_SPI2_Init(void);
static void MX_RNG_Init(void);
/* USER CODE BEGIN PFP */
/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
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
/* USER CODE END Boot_Mode_Sequence_0 */

/* USER CODE BEGIN Boot_Mode_Sequence_1 */
/* USER CODE END Boot_Mode_Sequence_1 */
  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */
  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();
/* USER CODE BEGIN Boot_Mode_Sequence_2 */
/* USER CODE END Boot_Mode_Sequence_2 */

  /* USER CODE BEGIN SysInit */
  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_SPI2_Init();
  MX_RNG_Init();
  /* USER CODE BEGIN 2 */
  /* USER CODE BEGIN 2 */
   TFT9341_ini(240, 320);
   TFT9341_FillScreen(TFT9341_GREEN);
   HAL_Delay(500);
   /* USER CODE END 2 */

   /* Infinite loop */
   /* USER CODE BEGIN WHILE */
   while (1)
   {
     /* USER CODE END WHILE */

     /* USER CODE BEGIN 3 */
     /* Тест: закрашиваем экран случайными цветами. */
//     LCD_Test_1();

     /* Тест: заливка экрана четырьмя прямоугольниками случайного цвета. */
     //LCD_Test_2();

     /* Тест: заливка экрана прямоугольниками случайного цвета, размера и расположения. */
     LCD_Test_3();

     /* Тест: вывод в случайных местах точек случайного цвета. */
     //LCD_Test_4();

     /* Тест: отрисовка параллельных отрезков во всю высоту экрана случайнми цветами. */
     //LCD_Test_5();

     /* Тест: черчение отрезков случайного цвета из случайной точки в случайную точку. */
     //LCD_Test_6();

     /* Тест: отрисовка прямоугольников последовательно от края к центру. */
     //LCD_Test_7();

     /* Тест: вывод окружности одинакового радиуса в различных местах экрана. */
     //LCD_Test_8();

     /* Тест: вывод отдельных символов на экран. */
     //LCD_Test_9();

     /* Тест: вывод целых строк с разной ориентацией. */
     //LCD_Test_10();
   }
   /* USER CODE END 3 */
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
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
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI48|RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_BYPASS;
  RCC_OscInitStruct.HSI48State = RCC_HSI48_ON;
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
  * @brief RNG Initialization Function
  * @param None
  * @retval None
  */
static void MX_RNG_Init(void)
{

  /* USER CODE BEGIN RNG_Init 0 */
  /* USER CODE END RNG_Init 0 */

  /* USER CODE BEGIN RNG_Init 1 */
  /* USER CODE END RNG_Init 1 */
  hrng.Instance = RNG;
  hrng.Init.ClockErrorDetection = RNG_CED_ENABLE;
  if (HAL_RNG_Init(&hrng) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN RNG_Init 2 */
  /* USER CODE END RNG_Init 2 */

}

/**
  * @brief SPI2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_SPI2_Init(void)
{

  /* USER CODE BEGIN SPI2_Init 0 */
  /* USER CODE END SPI2_Init 0 */

  /* USER CODE BEGIN SPI2_Init 1 */
  /* USER CODE END SPI2_Init 1 */
  /* SPI2 parameter configuration*/
  hspi2.Instance = SPI2;
  hspi2.Init.Mode = SPI_MODE_MASTER;
  hspi2.Init.Direction = SPI_DIRECTION_2LINES;
  hspi2.Init.DataSize = SPI_DATASIZE_8BIT;
  hspi2.Init.CLKPolarity = SPI_POLARITY_LOW;
  hspi2.Init.CLKPhase = SPI_PHASE_1EDGE;
  hspi2.Init.NSS = SPI_NSS_SOFT;
  hspi2.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_8;
  hspi2.Init.FirstBit = SPI_FIRSTBIT_MSB;
  hspi2.Init.TIMode = SPI_TIMODE_DISABLE;
  hspi2.Init.CRCCalculation = SPI_CRCCALCULATION_DISABLE;
  hspi2.Init.CRCPolynomial = 0x0;
  hspi2.Init.NSSPMode = SPI_NSS_PULSE_ENABLE;
  hspi2.Init.NSSPolarity = SPI_NSS_POLARITY_LOW;
  hspi2.Init.FifoThreshold = SPI_FIFO_THRESHOLD_01DATA;
  hspi2.Init.TxCRCInitializationPattern = SPI_CRC_INITIALIZATION_ALL_ZERO_PATTERN;
  hspi2.Init.RxCRCInitializationPattern = SPI_CRC_INITIALIZATION_ALL_ZERO_PATTERN;
  hspi2.Init.MasterSSIdleness = SPI_MASTER_SS_IDLENESS_00CYCLE;
  hspi2.Init.MasterInterDataIdleness = SPI_MASTER_INTERDATA_IDLENESS_00CYCLE;
  hspi2.Init.MasterReceiverAutoSusp = SPI_MASTER_RX_AUTOSUSP_DISABLE;
  hspi2.Init.MasterKeepIOState = SPI_MASTER_KEEP_IO_STATE_DISABLE;
  hspi2.Init.IOSwap = SPI_IO_SWAP_DISABLE;
  if (HAL_SPI_Init(&hspi2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN SPI2_Init 2 */
  /* USER CODE END SPI2_Init 2 */

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
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();
  __HAL_RCC_GPIOD_CLK_ENABLE();
  __HAL_RCC_GPIOG_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOB, LCD_RST_Pin|LCD_DC_Pin|LCD_CS_Pin, GPIO_PIN_SET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(TP_CS_GPIO_Port, TP_CS_Pin, GPIO_PIN_SET);

  /*Configure GPIO pins : PC1 PC4 PC5 */
  GPIO_InitStruct.Pin = GPIO_PIN_1|GPIO_PIN_4|GPIO_PIN_5;
  GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  GPIO_InitStruct.Alternate = GPIO_AF11_ETH;
  HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

  /*Configure GPIO pins : PA1 PA2 PA7 */
  GPIO_InitStruct.Pin = GPIO_PIN_1|GPIO_PIN_2|GPIO_PIN_7;
  GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  GPIO_InitStruct.Alternate = GPIO_AF11_ETH;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*Configure GPIO pins : LCD_RST_Pin LCD_DC_Pin LCD_CS_Pin */
  GPIO_InitStruct.Pin = LCD_RST_Pin|LCD_DC_Pin|LCD_CS_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

  /*Configure GPIO pin : PB13 */
  GPIO_InitStruct.Pin = GPIO_PIN_13;
  GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  GPIO_InitStruct.Alternate = GPIO_AF11_ETH;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

  /*Configure GPIO pins : PD8 PD9 */
  GPIO_InitStruct.Pin = GPIO_PIN_8|GPIO_PIN_9;
  GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  GPIO_InitStruct.Alternate = GPIO_AF7_USART3;
  HAL_GPIO_Init(GPIOD, &GPIO_InitStruct);

  /*Configure GPIO pin : PD11 */
  GPIO_InitStruct.Pin = GPIO_PIN_11;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(GPIOD, &GPIO_InitStruct);

  /*Configure GPIO pins : PA8 PA11 PA12 */
  GPIO_InitStruct.Pin = GPIO_PIN_8|GPIO_PIN_11|GPIO_PIN_12;
  GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  GPIO_InitStruct.Alternate = GPIO_AF10_OTG1_FS;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*Configure GPIO pin : TP_CS_Pin */
  GPIO_InitStruct.Pin = TP_CS_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
  HAL_GPIO_Init(TP_CS_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : PG11 PG13 */
  GPIO_InitStruct.Pin = GPIO_PIN_11|GPIO_PIN_13;
  GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  GPIO_InitStruct.Alternate = GPIO_AF11_ETH;
  HAL_GPIO_Init(GPIOG, &GPIO_InitStruct);

}

/* USER CODE BEGIN 4 */
/* Тест: закрашиваем экран случайными цветами. */
void LCD_Test_1(void)
{
  for (int i = 0; i < 20; i++) {
    TFT9341_FillScreen(TFT9341_RandColor());
    HAL_Delay(150);
  }
  HAL_Delay(500);
  TFT9341_FillScreen(TFT9341_BLACK);
}

/* Тест: заливка экрана четырьмя прямоугольниками случайного цвета. */
void LCD_Test_2(void)
{
  for (int i = 0; i < 20; i++) {
    TFT9341_FillRect(0, 0, TFT9341_WIDTH/2-1, TFT9341_HEIGHT/2-1, TFT9341_RandColor());
    HAL_Delay(100);
    TFT9341_FillRect(TFT9341_WIDTH/2, 0, TFT9341_WIDTH-1, TFT9341_HEIGHT/2-1, TFT9341_RandColor());
    HAL_Delay(100);
    TFT9341_FillRect(0, TFT9341_HEIGHT/2, TFT9341_WIDTH/2-1, TFT9341_HEIGHT-1, TFT9341_RandColor());
    HAL_Delay(100);
    TFT9341_FillRect(TFT9341_WIDTH/2, TFT9341_HEIGHT/2, TFT9341_WIDTH-1, TFT9341_HEIGHT-1, TFT9341_RandColor());
    HAL_Delay(100);
  }
  HAL_Delay(500);
  TFT9341_FillScreen(TFT9341_BLACK);
}

/* Тест: заливка экрана прямоугольниками случайного цвета, размера и расположения. */
void LCD_Test_3(void)
{
  for (int i = 0; i < 1000; i++) {
    TFT9341_FillRect(GetRandomNumber() % TFT9341_WIDTH,
      GetRandomNumber() % TFT9341_HEIGHT,
      GetRandomNumber() % TFT9341_WIDTH,
      GetRandomNumber() % TFT9341_HEIGHT,
      TFT9341_RandColor());
    HAL_Delay(10);
  }
  HAL_Delay(500);
  TFT9341_FillScreen(TFT9341_BLACK);
}

/* Тест: вывод в случайных местах точек случайного цвета. */
void LCD_Test_4(void)
{
  for (int i = 0; i < 15000; i++) {
    for (int j = 0; j < 100; j++) {
      TFT9341_DrawPixel(GetRandomNumber() % TFT9341_WIDTH,
        GetRandomNumber() % TFT9341_HEIGHT,
        TFT9341_BLACK);
    }
    TFT9341_DrawPixel(GetRandomNumber() % TFT9341_WIDTH,
      GetRandomNumber() % TFT9341_HEIGHT,
      TFT9341_RandColor());
    DelayMicro(100);
  }
  HAL_Delay(500);
}

/* Тест: отрисовка параллельных отрезков во всю высоту экрана случайнми цветами. */
void LCD_Test_5(void)
{
  for (int j = 0; j < 20; j++) {
    for(int i = 0; i < TFT9341_WIDTH; i++) {
      TFT9341_DrawLine(TFT9341_RandColor(), i, 0, i, TFT9341_HEIGHT-1);
    }
  }
  HAL_Delay(500);
  TFT9341_FillScreen(TFT9341_BLACK);
}

/* Тест: черчение отрезков случайного цвета из случайной точки в случайную точку. */
void LCD_Test_6(void)
{
  for (int i = 0; i < 1000; i++) {
    TFT9341_DrawLine(TFT9341_RandColor(),
      GetRandomNumber() % TFT9341_WIDTH,
      GetRandomNumber() % TFT9341_HEIGHT,
      GetRandomNumber() % TFT9341_WIDTH,
      GetRandomNumber() % TFT9341_HEIGHT);
    HAL_Delay(10);
  }
  HAL_Delay(500);
  TFT9341_FillScreen(TFT9341_BLACK);
}

/* Тест: отрисовка прямоугольников последовательно от края к центру. */
void LCD_Test_7(void)
{
  for (int j = 0; j < 20; j++) {
    for(int i = 0; i < TFT9341_WIDTH/2; i++) {
      TFT9341_DrawRect(TFT9341_RandColor(), i, i, TFT9341_WIDTH-i-1, TFT9341_HEIGHT-i-1);
    }
  }
  HAL_Delay(500);
  TFT9341_FillScreen(TFT9341_BLACK);
}

/* Тест: вывод окружности одинакового радиуса в различных местах экрана. */
void LCD_Test_8(void)
{
  for(int i = 0; i < 2000; i++) {
    TFT9341_DrawCircle(GetRandomNumber() % (TFT9341_WIDTH-40)+20,
      GetRandomNumber() % (TFT9341_HEIGHT-40)+20,
      20, TFT9341_RandColor());
    HAL_Delay(3);
  }
  HAL_Delay(500);
  TFT9341_FillScreen(TFT9341_BLACK);
}

/* Тест: вывод отдельных символов на экран. */
void LCD_Test_9(void)
{
  TFT9341_SetTextColor(TFT9341_YELLOW);
  TFT9341_SetBackColor(TFT9341_BLUE);
  TFT9341_SetFont(&Font24);
  TFT9341_DrawChar(10,10,'S');
  TFT9341_DrawChar(27,10,('t'));
  TFT9341_DrawChar(44,10,('m'));
  TFT9341_DrawChar(61,10,('3'));
  TFT9341_DrawChar(78,10,('2'));
  TFT9341_SetTextColor(TFT9341_GREEN);
  TFT9341_SetBackColor(TFT9341_RED);
  TFT9341_SetFont(&Font20);
  TFT9341_DrawChar(10,34,('S'));
  TFT9341_DrawChar(24,34,('t'));
  TFT9341_DrawChar(38,34,('m'));
  TFT9341_DrawChar(52,34,('3'));
  TFT9341_DrawChar(66,34,('2'));
  TFT9341_SetTextColor(TFT9341_BLUE);
  TFT9341_SetBackColor(TFT9341_YELLOW);
  TFT9341_SetFont(&Font16);
  TFT9341_DrawChar(10,54,('S'));
  TFT9341_DrawChar(21,54,('t'));
  TFT9341_DrawChar(32,54,('m'));
  TFT9341_DrawChar(43,54,('3'));
  TFT9341_DrawChar(54,54,('2'));
  TFT9341_SetTextColor(TFT9341_CYAN);
  TFT9341_SetBackColor(TFT9341_BLACK);
  TFT9341_SetFont(&Font12);
  TFT9341_DrawChar(10,70,('S'));
  TFT9341_DrawChar(17,70,('t'));
  TFT9341_DrawChar(24,70,('m'));
  TFT9341_DrawChar(31,70,('3'));
  TFT9341_DrawChar(38,70,('2'));
  TFT9341_SetTextColor(TFT9341_RED);
  TFT9341_SetBackColor(TFT9341_GREEN);
  TFT9341_SetFont(&Font8);
  TFT9341_DrawChar(10,82,('S'));
  TFT9341_DrawChar(15,82,('t'));
  TFT9341_DrawChar(20,82,('m'));
  TFT9341_DrawChar(25,82,('3'));
  TFT9341_DrawChar(30,82,('2'));
  TFT9341_SetTextColor(TFT9341_YELLOW);
  TFT9341_SetBackColor(TFT9341_BLUE);
  HAL_Delay(2000);
  TFT9341_FillScreen(TFT9341_BLACK);
}

/* Тест: вывод целых строк с разной ориентацией. */
void LCD_Test_10(void)
{
  for (int i = 0; i < 16; i++) {
    TFT9341_SetRotation(i % 4);
    TFT9341_SetFont(&Font24);
    TFT9341_FillScreen(TFT9341_BLACK);
    TFT9341_String(1, 100, "ABCDEF12345678");
    TFT9341_SetFont(&Font20);
    TFT9341_String(1, 124, "ABCDEFGHI12345678");
    TFT9341_SetFont(&Font16);
    TFT9341_String(1, 144, "ABCDEFGHIKL123456789");
    TFT9341_SetFont(&Font12);
    TFT9341_String(1, 160, "ABCDEFGHIKLMNOPQRSTUVWXY 123456789");
    TFT9341_SetFont(&Font8);
    TFT9341_String(1, 172, "ABCDEFGHIKLMNOPQRSTUVWXYZ 123456789ABCDEFGHIKL");
    HAL_Delay(2000);
  }
  HAL_Delay(10000);
  TFT9341_SetRotation(0);
}

uint32_t GetRandomNumber(void)
{
  uint32_t random32bit;
  HAL_RNG_GenerateRandomNumber(&hrng, &random32bit);
  return random32bit;
}
/* USER CODE END 4 */


/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
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
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
