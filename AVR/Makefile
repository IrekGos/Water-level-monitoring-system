PRG            = measure_water_level
OBJ            = ${PRG}.o UART.o
PROGRAMMER     = usbasp
PORT           = /dev/ttyUSB0
MCU_TARGET     = atmega88pa
AVRDUDE_TARGET = m88p
OPTIMIZE       = -O3
DEFS           =
LIBS           =
BAUDRATE       = 57600
BITCLOCK       = 5

HZ             = 1000000UL
SERIAL_PORT_BD = 2400

# You should not have to change anything below here.

CC             = avr-gcc

# Override is only needed by avr-lib build system.

override CFLAGS        = -g -std=c99 -DF_CPU=$(HZ) -Wall $(OPTIMIZE) -mmcu=$(MCU_TARGET) $(DEFS)
override LDFLAGS       = -Wl,-Map,$(PRG).map


OBJCOPY        = avr-objcopy
OBJDUMP        = avr-objdump
SIZE           = avr-size

all: $(PRG).elf lst text

$(PRG).elf: $(OBJ)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^ $(LIBS)

clean:
	rm -rf *.o *.elf *.eps *.bak *.hex *.bin *.srec
	rm -rf *.lst *.map $(EXTRA_CLEAN_FILES)

lst:  $(PRG).lst

%.lst: %.elf
	$(OBJDUMP) -h -S $< > $@

# Rules for building the .text rom images

text: hex bin srec

hex:  $(PRG).hex
bin:  $(PRG).bin
srec: $(PRG).srec

%.hex: %.elf
	$(OBJCOPY) -j .text -j .data -O ihex $< $@
	$(SIZE) --mcu=${MCU_TARGET} --format=avr $<

%.srec: %.elf
	$(OBJCOPY) -j .text -j .data -O srec $< $@

%.bin: %.elf
	$(OBJCOPY) -j .text -j .data -O binary $< $@

size:  $(PRG).elf
	$(SIZE) -C --mcu=$(MCU_TARGET) $(PRG).elf

install:  $(PRG).hex
	avrdude -p $(AVRDUDE_TARGET) -c $(PROGRAMMER) -P $(PORT) \
		-b $(BAUDRATE) -V -B $(BITCLOCK) -v -U flash:w:$(PRG).hex
        
# avrdude terminal mode
avrdude_terminal:
	avrdude -p $(AVRDUDE_TARGET) -c $(PROGRAMMER) -B $(BITCLOCK) -nt

miniterm:
	python -m serial.tools.miniterm $(PORT) $(SERIAL_PORT_BD)
