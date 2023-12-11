#include <stdbool.h>
#include <string.h>
#include <avr/interrupt.h>
#include <avr/sleep.h>
#include "UART.h"

volatile bool receive_complete;

void adc_init()
{
	ADMUX = _BV(REFS0); // reference -- AVcc 3.3V, input -- ADC0
	// ADC frequency -- 125 kHz (16 MHz / 128)
	ADCSRA = _BV(ADPS0) | _BV(ADPS1) | _BV(ADPS2); // preskaler -- 128
	DIDR0 = _BV(ADC0D);							   // turn off digital input at ADC0
	ADCSRA |= _BV(ADEN);						   // turn on the ADC
}

void timer1_init()
{
	// WGM1  = 0100 -- CTC top=OCR1A
	// CS1   = 101  -- prescaler 1024
	// frequency 1e6/(1024*(1+58593)) ≈ 1/60 Hz -- interrupt once per minute
	TCCR1B |= _BV(WGM12) | _BV(CS12) | _BV(CS10);
	// initialize counter
	TCNT1 = 0;
	// initialize compare value
	OCR1A = 58593;
}

uint16_t ADC_measure()
{
	ADCSRA |= _BV(ADSC); // start measure
	while (!(ADCSRA & _BV(ADIF)))
		;				 // wait for the result
	ADCSRA |= _BV(ADIF); // clear ADIF bit
	return ADC;
}

ISR(TIMER1_COMPA_vect)
{
	uint16_t adc = ADC_measure();
	printf("%d", adc);
}

ISR(USART_RX_vect)
{
	receive_complete = true;
}

int main()
{
	// turn off the analog comparator to save power
	ACSR = _BV(ACD);

	// initialize modules and sleep mode
	uart_init();
	adc_init();
	timer1_init();
	set_sleep_mode(SLEEP_MODE_IDLE);

	// configure input/output streams
	fdev_setup_stream(&uart_file, uart_transmit, uart_receive, _FDEV_SETUP_RW);
	stdin = stdout = stderr = &uart_file;

	bool is_enabled = false;
	receive_complete = false;
	char secret_key[50];

	// interrupts enable
	sei();

	while (1)
	{
		if (receive_complete)
		{
			fgets(secret_key, 50, stdin);
			if (!strncmp(secret_key, "Enter your secret key here", 24))
			{
				is_enabled = true;
				printf("1");
			}
			else
				printf("0");
		}
		if (is_enabled)
		{
			// Timer/Counter1, Output Compare A Match Interrupt Enable
			TIMSK1 |= _BV(OCIE1A);
			// run the first measure immediately
			TCNT1 = OCR1A - 100;
			// disable RX Complete Interrupt
			UCSR0B &= ~_BV(RXCIE0);
		}
		sleep_mode();
	}
}