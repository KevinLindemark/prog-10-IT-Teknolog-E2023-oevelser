import machine
import uasyncio as asyncio


class LCDMenu:
    def __init__(self, lcd, encoder, button):
        """Constructor, takes LCD, encoder and button pin object as arguments"""
        self.lcd = lcd
        self.encoder = encoder
        self.button = button

        self.menu_items = []  # A list to store menu items
        self.line = 1  # Index of the current menu
        self.highlight = 1  # Index of the selected item in the current menu
        self.shift = 0
        self.list_length = 0
        self.total_lines = 4
        self.selected_item = 0        
        
        self.encoder_last_state = None  # Store the last state of the encoder
        self.encoder_button_pressed = False  # Flag to track button press

        self.initialize_lcd()
        self.initialize_encoder()
        self.initialize_button()

    def button_callback(self, pin):
        """Callback function for button press"""
        if self.encoder_button_pressed == False:
            self.encoder_button_pressed = True

    def initialize_lcd(self):
        """Initialize and clear the LCD display"""
        self.lcd.clear()
        self.lcd.move_to(0, 0)

    def initialize_encoder(self):
        """Initialize the rotary encoder"""
        self.encoder_last_state = self.encoder.re_full_step()

    def initialize_button(self):
        """Initialize the button"""
        self.button.irq(handler=self.button_callback, trigger=machine.Pin.IRQ_FALLING)

    def add_menu_item(self, text, callback=None):
        """Add a menu item to the current menu"""
        self.menu_items.append({"text": text, "callback": callback})

    def display_menu(self):
        """Display the current menu"""
        self.lcd.clear()
        self.item = 1
        self.line = 1
        self.list_length = len(self.menu_items) #  the list of files so that it shows on the display
        short_list = self.menu_items[self.shift:self.shift+self.total_lines]
                
        for item in short_list:
            if self.highlight == self.line:
                self.lcd.move_to(1, self.line-1)
                self.lcd.putstr(item["text"])
                self.selected = self.line-1
            else:
                self.lcd.move_to(1, self.line-1)
                self.lcd.putstr(item["text"])
            self.line += 1
            self.lcd.move_to(0, self.selected)
            self.lcd.blink_cursor_on()

    async def navigate_menu(self):
        """Navigate menu system"""
        while True:
            # Read the current state of the encoder
            res = self.encoder.re_full_step()
            if res == -1:  # Turned Left
                if self.highlight > 1:
                    self.highlight -= 1
                else:
                    if self.shift > 0:
                        self.shift -= 1
                self.display_menu()
                # show_menu(file_list)

            if res == 1:    # Turned Right
                if self.highlight < self.total_lines:
                    self.highlight += 1
                else:
                    if self.shift+self.total_lines < self.list_length:
                        self.shift += 1

                self.display_menu()

            # Update the last state of the encoder
            self.encoder_last_state = res

            # Check if the button is pressed
            if self.encoder_button_pressed:

                #  add shift to selected to get correct callback
                callback = self.menu_items[self.selected+self.shift]["callback"]
                if callback:
                    callback()

            if self.encoder_button_pressed == True:
                #  add shift to selected to get correct callback
                await asyncio.sleep_ms(200)
                # Reset the button state
                self.encoder_button_pressed = False

    def run(self):
        """Start the navigation loop"""
        loop = asyncio.get_event_loop()
        loop.create_task(self.navigate_menu())
        loop.run_forever()
