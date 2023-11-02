#include <avr/io.h>
#include <stdio.h>

#define BAUD 2400

#define UBRR_VALUE ((F_CPU) / 16 / (BAUD)-1)

void uart_init();
int uart_transmit(char, FILE *);
int uart_receive(FILE *);

FILE uart_file;