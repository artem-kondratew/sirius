/**
  ******************************************************************************
  * @file    Templates/BootCM4_CM7/CM7/Inc/main.h
  * @author  MCD Application Team
  * @brief   Header for main.c module for Cortex-M7.
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

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

/* Includes ------------------------------------------------------------------*/
#include "stm32h7xx_hal.h"
#include "stm32h7xx_nucleo.h"

/* Exported types ------------------------------------------------------------*/
/* Exported constants --------------------------------------------------------*/
/* Definition for USARTx clock resources */
#define USARTx                           USART3
#define USARTx_CLK_ENABLE()              __HAL_RCC_USART3_CLK_ENABLE()
#define USARTx_RX_GPIO_CLK_ENABLE()      __HAL_RCC_GPIOD_CLK_ENABLE()
#define USARTx_TX_GPIO_CLK_ENABLE()      __HAL_RCC_GPIOD_CLK_ENABLE()

#define USARTx_FORCE_RESET()             __HAL_RCC_USART3_FORCE_RESET()
#define USARTx_RELEASE_RESET()           __HAL_RCC_USART3_RELEASE_RESET()

/* Definition for USARTx Pins */
#define USARTx_TX_PIN                    GPIO_PIN_8
#define USARTx_TX_GPIO_PORT              GPIOD
#define USARTx_TX_AF                     GPIO_AF7_USART3
#define USARTx_RX_PIN                    GPIO_PIN_9
#define USARTx_RX_GPIO_PORT              GPIOD
#define USARTx_RX_AF                     GPIO_AF7_USART3

/* Exported macro ------------------------------------------------------------*/
/* Exported functions ------------------------------------------------------- */

#endif /* __MAIN_H */













///**
//  ******************************************************************************
//  * @file    Templates/BootCM4_CM7/CM7/Inc/main.h
//  * @author  MCD Application Team
//  * @brief   Header for main.c module for Cortex-M7.
//  ******************************************************************************
//  * @attention
//  *
//  * Copyright (c) 2018 STMicroelectronics.
//  * All rights reserved.
//  *
//  * This software is licensed under terms that can be found in the LICENSE file
//  * in the root directory of this software component.
//  * If no LICENSE file comes with this software, it is provided AS-IS.
//  *
//  ******************************************************************************
//  */
//
///* Define to prevent recursive inclusion -------------------------------------*/
//#ifndef __MAIN_H
//#define __MAIN_H
//
///* Includes ------------------------------------------------------------------*/
//#include "stm32h7xx_hal.h"
//#include "stm32h7xx_nucleo.h"
//
///* Exported types ------------------------------------------------------------*/
///* Exported constants --------------------------------------------------------*/
///* Definition for USARTx clock resources */
//#define USARTx                           USART2
//#define USARTx_CLK_ENABLE()              __HAL_RCC_USART2_CLK_ENABLE()
//#define USARTx_RX_GPIO_CLK_ENABLE()      __HAL_RCC_GPIOD_CLK_ENABLE()
//#define USARTx_TX_GPIO_CLK_ENABLE()      __HAL_RCC_GPIOD_CLK_ENABLE()
//
//#define USARTx_FORCE_RESET()             __HAL_RCC_USART2_FORCE_RESET()
//#define USARTx_RELEASE_RESET()           __HAL_RCC_USART2_RELEASE_RESET()
//
///* Definition for USARTx Pins */
//#define USARTx_TX_PIN                    GPIO_PIN_5
//#define USARTx_TX_GPIO_PORT              GPIOD
//#define USARTx_TX_AF                     GPIO_AF7_USART2
//#define USARTx_RX_PIN                    GPIO_PIN_6
//#define USARTx_RX_GPIO_PORT              GPIOD
//#define USARTx_RX_AF                     GPIO_AF7_USART2
//
///* Exported macro ------------------------------------------------------------*/
///* Exported functions ------------------------------------------------------- */
//
//#endif /* __MAIN_H */


