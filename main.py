from dataclasses import field
import flet as ft
from sympy import sympify, N, sin, cos, tan, sqrt

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

@ft.control
class SciButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.BLUE_GREY_900
    color: ft.Colors = ft.Colors.WHITE

class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()
        
        self.width = 350
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = ft.BorderRadius.all(20)
        self.padding = 15
        
        # Small text for expression history
        self.expression_display = ft.Text(
            value="", 
            color=ft.Colors.WHITE54, 
            size=15, 
            text_align=ft.TextAlign.RIGHT
        )
        
        # Main result text
        self.result = ft.Text(value="0", color=ft.Colors.WHITE, size=40, text_align=ft.TextAlign.RIGHT)

        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.expression_display], alignment=ft.MainAxisAlignment.END),
                ft.Row(controls=[self.result], alignment=ft.MainAxisAlignment.END),
                
                # [ROW 1] Scientific
                ft.Row(
                    controls=[
                        SciButton(content="sin", on_click=self.button_clicked),
                        SciButton(content="cos", on_click=self.button_clicked),
                        SciButton(content="tan", on_click=self.button_clicked),
                        SciButton(content="√", on_click=self.button_clicked),
                    ]
                ),
                
                # [ROW 2] Parentheses & Edit
                ft.Row(
                    controls=[
                        SciButton(content="(", on_click=self.button_clicked),
                        SciButton(content=")", on_click=self.button_clicked),
                        ExtraActionButton(content="CE", on_click=self.button_clicked),
                        ExtraActionButton(content="⬅", on_click=self.button_clicked),
                    ]
                ),

                # [ROW 3] Standard Operators
                ft.Row(
                    controls=[
                        ExtraActionButton(content="AC", on_click=self.button_clicked),
                        ExtraActionButton(content="+/-", on_click=self.button_clicked),
                        ExtraActionButton(content="%", on_click=self.button_clicked),
                        ActionButton(content="/", on_click=self.button_clicked),
                    ]
                ),
                
                # [ROW 4] 7-9
                ft.Row(
                    controls=[
                        DigitButton(content="7", on_click=self.button_clicked),
                        DigitButton(content="8", on_click=self.button_clicked),
                        DigitButton(content="9", on_click=self.button_clicked),
                        ActionButton(content="*", on_click=self.button_clicked),
                    ]
                ),
                
                # [ROW 5] 4-6
                ft.Row(
                    controls=[
                        DigitButton(content="4", on_click=self.button_clicked),
                        DigitButton(content="5", on_click=self.button_clicked),
                        DigitButton(content="6", on_click=self.button_clicked),
                        ActionButton(content="-", on_click=self.button_clicked),
                    ]
                ),
                
                # [ROW 6] 1-3
                ft.Row(
                    controls=[
                        DigitButton(content="1", on_click=self.button_clicked),
                        DigitButton(content="2", on_click=self.button_clicked),
                        DigitButton(content="3", on_click=self.button_clicked),
                        ActionButton(content="+", on_click=self.button_clicked),
                    ]
                ),
                
                # [ROW 7] 0, ., =
                ft.Row(
                    controls=[
                        DigitButton(content="0", expand=2, on_click=self.button_clicked),
                        DigitButton(content=".", on_click=self.button_clicked),
                        ActionButton(content="=", on_click=self.button_clicked),
                    ]
                ),
            ]
        )

    # Helper: Adds spaces to numbers (e.g. 1 000 000)
    def format_thousands(self, value):
        try:
            clean_val = str(value).replace(" ", "")
            if "." in clean_val:
                integer_part, decimal_part = clean_val.split(".", 1)
                formatted_int = "{:,}".format(int(integer_part)).replace(",", " ")
                return f"{formatted_int}.{decimal_part}"
            else:
                return "{:,}".format(int(clean_val)).replace(",", " ")
        except ValueError:
            return value

    def button_clicked(self, e):
        data = e.control.content
        print(f"Button clicked = {data}")

        # --- CLEAR & RESET ---
        if data == "AC":
            self.reset()
            
        elif data == "CE": 
            self.result.value = "0"

        elif data == "⬅": 
            current_val = str(self.result.value)
            if len(current_val) > 1:
                self.result.value = self.format_thousands(current_val[:-1])
            else:
                self.result.value = "0"

        # --- DIGITS ---
        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            clean_current = str(self.result.value).replace(" ", "")
            
            if clean_current == "0" or self.new_operand:
                clean_current = data
                self.new_operand = False
            else:
                clean_current = clean_current + data
            
            self.result.value = self.format_thousands(clean_current)

        # --- SCIENTIFIC FUNCTIONS ---
        elif data in ("sin", "cos", "tan", "√"):
            func_map = {"√": "sqrt"}
            func_name = func_map.get(data, data)
            
            # Start a function group
            self.current_expression += f"{func_name}("
            self.expression_display.value = self.current_expression
            self.new_operand = True

        # --- PARENTHESES ---
        elif data in ("(", ")"):
            clean_current = str(self.result.value).replace(" ", "")
            
            if data == "(":
                self.current_expression += "("
                self.new_operand = True
            elif data == ")":
                # Check if we just closed a group to avoid double-adding numbers
                if self.current_expression.endswith(")"):
                     self.current_expression += ")"
                else:
                     self.current_expression += clean_current + ")"
                
                self.new_operand = True
                
            self.expression_display.value = self.current_expression

        # --- OPERATORS ---
        elif data in ("+", "-", "*", "/"):
            clean_current = str(self.result.value).replace(" ", "")
            
            # If expression ends in ')', just add operator, don't add the number on screen
            if self.current_expression.endswith(")"):
                self.current_expression += data
            else:
                self.current_expression += clean_current + data
                
            self.expression_display.value = self.current_expression
            self.new_operand = True 

        # --- EQUALS ---
        elif data == "=":
            clean_current = str(self.result.value).replace(" ", "")
            
            # If expression ends in ')', use it as is. Otherwise add the last number.
            if self.current_expression.endswith(")"):
                final_expression = self.current_expression
            else:
                final_expression = self.current_expression + clean_current
            
            # Auto-balance parentheses
            open_count = final_expression.count("(")
            close_count = final_expression.count(")")
            final_expression += ")" * (open_count - close_count)
            
            self.expression_display.value = final_expression + "="
            self.calculate_result(final_expression)
            
            # Reset history but keep result
            self.current_expression = ""
            self.new_operand = True

        elif data == "%":
            clean_current = str(self.result.value).replace(" ", "")
            val = float(clean_current) / 100
            self.result.value = self.format_number(val)

        elif data == "+/-":
            clean_current = str(self.result.value).replace(" ", "")
            if float(clean_current) > 0:
                val = "-" + clean_current
            elif float(clean_current) < 0:
                val = str(abs(float(clean_current)))
            else:
                val = clean_current
            self.result.value = self.format_thousands(val)

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
            final_val = self.format_number(float(result_val))
            self.result.value = self.format_thousands(final_val)
            
        except Exception as e:
            print(f"Error: {e}")
            self.result.value = "Error"
            self.current_expression = ""

    def reset(self):
        self.current_expression = ""
        self.new_operand = True
        if hasattr(self, 'result'): self.result.value = "0"
        if hasattr(self, 'expression_display'): self.expression_display.value = ""

def main(page: ft.Page):
    page.title = "Scientific Calc"
    page.bgcolor = ft.Colors.BLACK
    page.scroll = "adaptive"
    
    calc = CalculatorApp()
    page.add(calc)

ft.run(main)