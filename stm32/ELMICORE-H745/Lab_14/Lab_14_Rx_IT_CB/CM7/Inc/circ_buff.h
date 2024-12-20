
#ifndef __CIRC_BUFF_H
#define __CIRC_BUFF_H

#ifdef __cplusplus
 extern "C" {
#endif

#include "stm32h7xx_hal.h"
#include <stdbool.h>

/* Кольцевой буфер вида "Always Keep One Slot Open" */
typedef struct {
  uint32_t uhStart;   /* index of oldest element */
  uint32_t uhEnd;     /* index at which to write new element */
  uint8_t *pElems;    /* vector of elements */
  uint32_t uhMASK;
} SCircBuff;

void CircBuffInit(SCircBuff *cb, uint8_t *elems, uint32_t size);
bool CircBuffIsEmpty(SCircBuff *cb);
void CircBuffRead(SCircBuff *cb, uint8_t *elem);
void CircBuffWrite(SCircBuff *cb, uint8_t elem);

#ifdef __cplusplus
}
#endif

#endif /* __CIRC_BUFF_H */
