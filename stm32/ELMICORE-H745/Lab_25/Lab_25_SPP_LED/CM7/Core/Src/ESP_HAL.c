/*
 * ESP_HAL.c
 */

#include "UartRingbuffer_multi.h"
#include "ESP_HAL.h"
#include "stdio.h"
#include "string.h"
#include "stdlib.h"
#include "main.h"

extern UART_HandleTypeDef huart6;
extern UART_HandleTypeDef huart3;

#define esp_uart &huart6
#define pc_uart &huart3


char buffer[64];
char datatosend[1024];
char data[80];


void ESP_Init(char *name, char *pin)
{
	Ringbuf_init();

	/*** RESET ******************************************************************/
	Uart_sendstring("AT+RST\r\n", esp_uart);
	Uart_sendstring("\r\nRESETTING.", pc_uart);
	for (int i=0; i<5; i++)
	{
		Uart_sendstring(".", pc_uart);
		HAL_Delay(1000);
	}
	Uart_sendstring("OK\r\n", pc_uart);

	/*** AT *********************************************************************/
	/* Test AT Startup */
	Uart_flush(esp_uart);
	Uart_sendstring("AT\r\n", esp_uart);
	while (!(Wait_for("OK\r\n", esp_uart)));
	Uart_sendstring("AT---->OK\r\n", pc_uart);

	/*** AT+BTINIT=1 ************************************************************/
	/* Classic Bluetooth initialization */
  Uart_flush(esp_uart);
  Uart_sendstring("AT+BTINIT=1\r\n", esp_uart);
  while (!(Wait_for("OK\r\n", esp_uart)));
  Uart_sendstring("BTINIT---->1\r\n", pc_uart);


  /*** AT+BTSPPINIT=2 *********************************************************/
  /* Classic Bluetooth SPP profile initialization, and the role is set to slave */
  Uart_flush(esp_uart);
  Uart_sendstring("AT+BTSPPINIT=2\r\n", esp_uart);
  while (!(Wait_for("OK\r\n", esp_uart)));
  Uart_sendstring("BTSPPINIT---->2\r\n", pc_uart);


  /*** AT+BTNAME="name" *******************************************************/
  /* Set Classic Bluetooth device name */
  Uart_flush(esp_uart);
  sprintf(data, "AT+BTNAME=\"%s\"\r\n", name);
  Uart_sendstring(data, esp_uart);
  while (!(Wait_for("OK\r\n", esp_uart)));
  Uart_sendstring("BTNAME---->OK\r\n", pc_uart);


  /*** AT+BTSCANMODE=2 ********************************************************/
  /* Set Classic Bluetooth scan mode to discoverable and connectable */
  Uart_flush(esp_uart);
  Uart_sendstring("AT+BTSCANMODE=2\r\n", esp_uart);
  while (!(Wait_for("OK\r\n", esp_uart)));
  Uart_sendstring("BTSCANMODE---->2\r\n", pc_uart);


  /*** AT+BTSECPARAM=3,1,"pin" ************************************************/
  /* Set Classic Bluetooth security parameters */
  Uart_flush(esp_uart);
  sprintf(data, "AT+BTSECPARAM=3,1,\"%s\"\r\n", pin);
  Uart_sendstring(data, esp_uart);
  while (!(Wait_for("OK\r\n", esp_uart)));
  Uart_sendstring("BTSECPARAM---->OK\r\n", pc_uart);


  /*** AT+BTSPPSTART **********************************************************/
  /* Start Classic Bluetooth SPP profile */
  Uart_flush(esp_uart);
  Uart_sendstring("AT+BTSPPSTART\r\n", esp_uart);
  while (!(Wait_for("OK\r\n", esp_uart)));
  Uart_sendstring("BTSPPSTART---->OK\r\n", pc_uart);

  Uart_sendstring("READY!\r\n", pc_uart);
}


void Server_Send(char *str, int Link_ID)
{
	int len = strlen(str);

	sprintf(data, "AT+BTSPPSEND=%d,%d\r\n", Link_ID, len);
  Uart_sendstring(data, esp_uart);
  while (!(Wait_for(">", esp_uart)));
  Uart_sendstring (str, esp_uart);
  while (!(Wait_for("OK", esp_uart)));
}

void Server_Handle(char *str, int Link_ID)
{
	if (!(strcmp(str, "ledon")))
	{
    HAL_GPIO_WritePin(LD1_GPIO_Port, LD1_Pin, 1);

    sprintf(datatosend, "ledon");
		Server_Send(datatosend, Link_ID);
	}
	else if (!(strcmp (str, "ledoff")))
	{
    HAL_GPIO_WritePin(LD1_GPIO_Port, LD1_Pin, 0);

    sprintf(datatosend, "ledoff");
		Server_Send(datatosend, Link_ID);
	}
}

void Server_Process(void)
{
    /* Connection Index always 0.
     * ESP32 AT User Guide: "Only 0 is supported for the single connection right now".
     */
    char Link_ID = 0;

    while (!(Wait_for("+BTDATA:", esp_uart)));

    while (!(Copy_upto(",", buffer, esp_uart)));

    int len = atoi(buffer);
    sprintf(buffer, "Receive %d bytes\r\n", len);
    Uart_sendstring(buffer, pc_uart);

    memset(buffer, 0, 64);
    while (!(Copy_upto("\r\n", buffer, esp_uart)));
    Server_Send(buffer, Link_ID);


//    if (Look_for("ledon", buffer) == 1)
//        Server_Handle("ledon", Link_ID);
//    else if (Look_for("ledoff", buffer) == 1)
//        Server_Handle("ledoff", Link_ID);
}
