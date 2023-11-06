#include "UART.h"

// initialize UART
void uart_init()
{
	// set baudrate
	UBRR0 = UBRR_VALUE;
	// turn on transmitter and receiver
	UCSR0B = _BV(RXEN0) | _BV(TXEN0);
	// set 8n1 format
	UCSR0C = _BV(UCSZ00) | _BV(UCSZ01);
	// RX Complete Interrupt Enable
	UCSR0B |= _BV(RXCIE0);
}

// transmit one char
int uart_transmit(char data, FILE *stream)
{
	// wait until the transmitter is ready
	while (!(UCSR0A & _BV(UDRE0)))
		;
	UDR0 = data;
	return 0;
}

// read one char
int uart_receive(FILE *stream)
{
	// wait until char is available
	while (!(UCSR0A & _BV(RXC0)))
		;
	return UDR0;
}