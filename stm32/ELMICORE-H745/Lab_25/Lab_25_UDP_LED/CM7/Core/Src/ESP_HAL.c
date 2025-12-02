/*
 * ESP_HAL.c
 */

#include "UartRingbuffer_multi.h"
#include "ESP_HAL.h"
#include "stdio.h"
#include "string.h"
#include "main.h"

extern UART_HandleTypeDef huart6;
extern UART_HandleTypeDef huart3;

#define esp_uart &huart6
#define pc_uart &huart3


char buffer[64];
char datatosend[1024];
char data[80];


void ESP_Init(char *SSID, char *PASSWD)
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

  /*** AT+CWMODE=2 ************************************************************/
  /* Set the Wi-Fi mode to softAP */
  Uart_flush(esp_uart);
  Uart_sendstring("AT+CWMODE=2\r\n", esp_uart);
  while (!(Wait_for("OK\r\n", esp_uart)));
  Uart_sendstring("CW MODE---->1\r\n", pc_uart);

  /*** AT+CIPMUX **************************************************************/
  /* Enable multiple connections */
  Uart_flush(esp_uart);
  Uart_sendstring("AT+CIPMUX=1\r\n", esp_uart);
  while (!(Wait_for("OK\r\n", esp_uart)));
  Uart_sendstring("CIPMUX---->OK\r\n", pc_uart);

  /*** AT+CWSAP="SSID","PASSWD",5,3 *******************************************/
  /* Set softAP */
  Uart_flush(esp_uart);
  Uart_sendstring("Setting AP ...\r\n", pc_uart);
  sprintf(data, "AT+CWSAP=\"%s\",\"%s\",5,3\r\n", SSID, PASSWD);
  Uart_sendstring(data, esp_uart);
  while (!(Wait_for("OK\r\n", esp_uart)));
  sprintf(data, "Settled to \"%s\"\r\n", SSID);
  Uart_sendstring(data, pc_uart);

  /*** AT+CIPAP? **************************************************************/
  /* Query softAP information */
  Uart_flush(esp_uart);
  Uart_sendstring("AT+CIPAP?\r\n", esp_uart);
  while (!(Wait_for("+CIPAP:ip:\"", esp_uart)));
  while (!(Copy_upto("\"", buffer, esp_uart)));
  while (!(Wait_for("OK\r\n", esp_uart)));
  int len = strlen(buffer);
  buffer[len-1] = '\0';
  sprintf(data, "IP ADDR: %s\r\n", buffer);
  Uart_sendstring(data, pc_uart);

  /*** AT+CIPSTART ************************************************************/
  /* Create a UDP transmission */
  /* Listening for UDP traffic on port 7 from all adresses */
//  Uart_flush(esp_uart);
//  Uart_sendstring("AT+CIPSTART=0,\"UDP\",\"0.0.0.0\",7,7,2\r\n", esp_uart);
//  while (!(Wait_for("OK\r\n", esp_uart)));
//  Uart_sendstring("Create a UDP transmission---->OK\r\n", pc_uart);

  Uart_flush(esp_uart);
  Uart_sendstring("AT+CIPSERVER=1,80\r\n", esp_uart);
  while (!(Wait_for("OK\r\n", esp_uart)));
  Uart_sendstring("TCP Server on Port 80---->OK\r\n", pc_uart);
}


void Server_Send(char *str, int Link_ID)
{
	int len = strlen(str);

	sprintf(data, "AT+CIPSEND=%d,%d\r\n", Link_ID, len);
	Uart_sendstring(data, esp_uart);
	while (!(Wait_for(">", esp_uart)));
	Uart_sendstring (str, esp_uart);
	while (!(Wait_for("SEND OK", esp_uart)));
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
	char Link_ID;

	while (!(Get_after("+IPD,", 1, &Link_ID, esp_uart)));

	Link_ID -= 48; // Char to Int

	while (!(Copy_upto("\r\n", buffer, esp_uart)));

	if (Look_for("ledon", buffer) == 1)
		Server_Handle("ledon", Link_ID);
	else if (Look_for("ledoff", buffer) == 1)
		Server_Handle("ledoff", Link_ID);
}
