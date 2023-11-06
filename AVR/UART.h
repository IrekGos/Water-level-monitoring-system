#include <stdio.h>
#include <avr/io.h>

#define BAUD 4800

#define UBRR_VALUE ((F_CPU) / 16 / (BAUD)-1)

void uart_init();
int uart_transmit(char, FILE *);
int uart_receive(FILE *);

FILE uart_file;