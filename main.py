from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.card import MDCard
from kivy.clock import Clock

class RomanDecimalConverterApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')

        card = MDCard(orientation="vertical", padding=40, size_hint=(None, None), size=(700, 500), elevation=2)
        card.add_widget(MDLabel(text="Romano <-> Decimal", halign="center", font_style="H5"))

        input_label = MDLabel(text="Digite um número romano ou decimal:", halign='center')
        card.add_widget(input_label)

        self.input_text = MDTextField(multiline=False, size_hint=(1, None), mode="fill")
        self.input_text.bind(on_text_validate=self.convert)
        card.add_widget(self.input_text)

        button_layout = AnchorLayout(anchor_x='center')
        self.convert_button = MDFillRoundFlatButton(text="=", size_hint=(0.25, None))
        self.convert_button.bind(on_press=self.convert)
        button_layout.add_widget(self.convert_button)
        card.add_widget(button_layout)

        self.result_label = MDLabel(text="", halign='center')
        card.add_widget(self.result_label)

        anchor_layout.add_widget(card)

        Clock.schedule_once(self.set_focus, 0.1)

        return anchor_layout

    def set_focus(self, dt):
        self.input_text.focus = True

    def convert(self, _):
        try:
            value = self.input_text.text.strip().upper()
            if not value:
                raise ValueError("Por favor, digite um número romano ou decimal.")
            
            if value.isdigit():
                if int(value) == 0:
                    raise ValueError("O número zero não tem representação no sistema de numeração romano!")
                else:
                    result = decimal_to_roman(int(value))
                    result_text = f"{value} = {result}"
            else:
                result = roman_to_decimal(value)
                result_text = f"{value} = {result}"

            self.result_label.text = result_text
        except ValueError as e:
            self.result_label.text = str(e)


def roman_to_decimal(roman):
    roman_numerals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    decimal = 0
    prev_value = 0

    for char in reversed(roman):
        if char not in roman_numerals:
            raise ValueError("Este número contém caracteres inválidos.")

        value = roman_numerals[char]
        if value < prev_value:
            decimal -= value
        else:
            decimal += value
        prev_value = value

    return decimal


def decimal_to_roman(decimal):
    roman_numerals = {1: 'I', 4: 'IV', 5: 'V', 9: 'IX', 10: 'X', 40: 'XL', 50: 'L', 90: 'XC', 100: 'C', 400: 'CD', 500: 'D', 900: 'CM', 1000: 'M'}
    result = ''
    for value, numeral in sorted(roman_numerals.items(), reverse=True):
        while decimal >= value:
            result += numeral
            decimal -= value
    return result


if __name__ == "__main__":
    RomanDecimalConverterApp().run()
