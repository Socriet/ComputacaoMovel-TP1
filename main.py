from dataclasses import field
import flet as ft
from sympy import sympify, N 

@ft.control
class CalcButton(ft.Button):
    expand: int = field(default_factory=lambda: 1)

@ft.control
class DigitButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.WHITE_24
    color: ft.Colors = ft.Colors.WHITE

@ft.control
class ActionButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.ORANGE
    color: ft.Colors = ft.Colors.WHITE

@ft.control
class ExtraActionButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.BLUE_GREY_100
    color: ft.Colors = ft.Colors.BLACK

class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()
        
        self.width = 350
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = ft.BorderRadius.all(20)
        self.padding = 20
        
        # [NEW] Small text display for the full expression (Objective 2)
        self.expression_display = ft.Text(
            value="", 
            color=ft.Colors.WHITE54, 
            size=15, 
            text_align=ft.TextAlign.RIGHT
        )
        
        # Main result display
        self.result = ft.Text(value="0", color=ft.Colors.WHITE, size=40, text_align=ft.TextAlign.RIGHT)

        self.content = ft.Column(
            controls=[
                # Row for the expression history
                ft.Row(
                    controls=[self.expression_display],
                    alignment=ft.MainAxisAlignment.END,
                ),
                # Row for the current result
                ft.Row(
                    controls=[self.result],
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.Row(
                    controls=[
                        ExtraActionButton(content="AC", on_click=self.button_clicked),
                        ExtraActionButton(content="+/-", on_click=self.button_clicked),
                        ExtraActionButton(content="%", on_click=self.button_clicked),
                        ActionButton(content="/", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="7", on_click=self.button_clicked),
                        DigitButton(content="8", on_click=self.button_clicked),
                        DigitButton(content="9", on_click=self.button_clicked),
                        ActionButton(content="*", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="4", on_click=self.button_clicked),
                        DigitButton(content="5", on_click=self.button_clicked),
                        DigitButton(content="6", on_click=self.button_clicked),
                        ActionButton(content="-", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="1", on_click=self.button_clicked),
                        DigitButton(content="2", on_click=self.button_clicked),
                        DigitButton(content="3", on_click=self.button_clicked),
                        ActionButton(content="+", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(
                            content="0", expand=2, on_click=self.button_clicked
                        ),
                        DigitButton(content=".", on_click=self.button_clicked),
                        ActionButton(content="=", on_click=self.button_clicked),
                    ]
                ),
            ]
        )

    def button_clicked(self, e):
        data = e.control.content
        print(f"Button clicked with data = {data}")

        if data == "AC":
            self.reset()
        
        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if self.result.value == "0" or self.new_operand:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value = self.result.value + data

        elif data in ("+", "-", "*", "/"):
            self.current_expression += self.result.value + data
            
            self.expression_display.value = self.current_expression
            
    
            self.new_operand = True 

        elif data == "=":
    
            final_expression = self.current_expression + self.result.value
            
            self.expression_display.value = final_expression + "="
            
            self.calculate_result(final_expression)
            
            self.current_expression = ""
            self.new_operand = True

        elif data == "%":
            val = float(self.result.value) / 100
            self.result.value = self.format_number(val)

        elif data == "+/-":
            if float(self.result.value) > 0:
                self.result.value = "-" + str(self.result.value)
            elif float(self.result.value) < 0:
                self.result.value = str(self.format_number(abs(float(self.result.value))))

        self.update()

    def format_number(self, num):
        if num % 1 == 0:
            return int(num)
        else:
            return num

    def calculate_result(self, expression):
        try:
            expr = sympify(expression)
            result_val = N(expr)
            
            self.result.value = str(self.format_number(float(result_val)))
            
        except Exception as e:
            print(f"Calculation Error: {e}")
            self.result.value = "Error"
            self.current_expression = ""

    def reset(self):
        self.current_expression = ""
        self.new_operand = True
        if hasattr(self, 'result'): self.result.value = "0"
        if hasattr(self, 'expression_display'): self.expression_display.value = ""

def main(page: ft.Page):
    page.title = "Calc App"
    page.bgcolor = ft.Colors.BLACK
    
    calc = CalculatorApp()

    
    page.add(calc)

ft.run(main)