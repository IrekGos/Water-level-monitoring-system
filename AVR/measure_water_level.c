#include <avr/interrupt.h>
#include <avr/sleep.h>
#include "UART.h"

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
	// frequency 1e6/(1024*(1+976)) ≈ 1 Hz -- interrupt once per second
	TCCR1B |= _BV(WGM12) | _BV(CS12) | _BV(CS10);
	TIMSK1 |= _BV(OCIE1A);
	// initialize counter
	TCNT1 = 0;
	// initialize compare value
	OCR1A = 976;
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

	// interrupts enable
	sei();

	while (1)
	{
		sleep_mode();
	}
}