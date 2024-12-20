
#include "circ_buff.h"

/* Инициализация кольцевого буфера.
  Параметры:
    cb - указатель на экземпляр кольцевого буфера;
    elems - указатель на массив элементов буфера;
    size - размер буфера, включая пустой элемент, должен быть РАВЕН СТЕПЕНИ ДВОЙКИ!
  Возвращаемое значение: нет
*/
void CircBuffInit(SCircBuff *cb, uint8_t *elems, uint32_t size)
{
  cb->uhStart = 0;
  cb->uhEnd = 0;
  cb->pElems = elems;
  cb->uhMASK = size - 1;
}

bool CircBuffIsEmpty(SCircBuff *cb)
{
  return (cb->uhEnd == cb->uhStart);
}

/* Read oldest element. App must ensure !IsEmpty() first. */
void CircBuffRead(SCircBuff *cb, uint8_t *elem)
{
  *elem = cb->pElems[cb->uhStart++];
  cb->uhStart &= cb->uhMASK;  // Переход на начало буфера.
}

/* Write an element, overwriting oldest element if buffer is full. */
void CircBuffWrite(SCircBuff *cb, uint8_t elem)
{
  cb->pElems[cb->uhEnd++] = elem; // Write an element.
  cb->uhEnd &= cb->uhMASK; // Переход на начало буфера.
  if(cb->uhEnd == cb->uhStart)
    cb->uhStart = (cb->uhStart + 1) & cb->uhMASK; // Full, overwrite oldest element.
}
