import pyperclip  
from dataclasses import field
from typing import Callable
from datetime import datetime
import flet as ft
from sympy import sympify, N, sin, cos, tan, sqrt


@ft.control
class HistoryItem(ft.Container):
    index: int = 0
    expression: str = ""
    result: str = ""
    timestamp: str = ""
    on_delete: Callable[["HistoryItem"], None] = field(default=lambda task: None)

    def init(self):
        self.padding = 10
     
        self.border = ft.Border(bottom=ft.BorderSide(1, ft.Colors.WHITE12))
        
        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
        
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Text(f"#{self.index} - {self.timestamp}", size=10, color=ft.Colors.WHITE54),
                        ft.Text(self.expression, size=12, color=ft.Colors.WHITE70),
                        ft.Text(f"= {self.result}", size=16, color=ft.Colors.ORANGE, weight=ft.FontWeight.BOLD),
                    ]
                ),
              
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.COPY, 
                            icon_size=18, 
                            tooltip="Copy Result", 
                            on_click=self.copy_clicked
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE, 
                            icon_size=18, 
                            icon_color=ft.Colors.RED_400,
                            tooltip="Delete", 
                            on_click=self.delete_clicked
                        ),
                    ]
                )
            ]
        )

    def copy_clicked(self, e):
        
        try:
            pyperclip.copy(self.result)
            e.page.snack_bar = ft.SnackBar(ft.Text(f"Copied: {self.result}"))
            e.page.snack_bar.open = True
            e.page.update()
        except Exception as ex:
            print(f"Clipboard error: {ex}")
            e.control.icon_color = ft.Colors.RED
            e.control.tooltip = "Clipboard failed"
            e.control.update()

    def delete_clicked(self, e):
        self.on_delete(self)


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
        self.history_counter = 1 
        
        self.width = 350
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = ft.BorderRadius.all(20)
        self.padding = 15
        
     
        self.expression_display = ft.Text(
            value="", color=ft.Colors.WHITE54, size=15, text_align=ft.TextAlign.RIGHT
        )
        self.result = ft.Text(value="0", color=ft.Colors.WHITE, size=40, text_align=ft.TextAlign.RIGHT)

      
        self.keypad_container = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        SciButton(content="sin", on_click=self.button_clicked),
                        SciButton(content="cos", on_click=self.button_clicked),
                        SciButton(content="tan", on_click=self.button_clicked),
                        SciButton(content="√", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        SciButton(content="(", on_click=self.button_clicked),
                        SciButton(content=")", on_click=self.button_clicked),
                        ExtraActionButton(content="CE", on_click=self.button_clicked),
                        ExtraActionButton(content="⬅", on_click=self.button_clicked),
                    ]
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
                        DigitButton(content="0", expand=2, on_click=self.button_clicked),
                        DigitButton(content=".", on_click=self.button_clicked),
                        ActionButton(content="=", on_click=self.button_clicked),
                    ]
                ),
            ]
        )

       
        self.history_list = ft.Column(scroll=ft.ScrollMode.AUTO, height=400)
        self.history_container = ft.Container(
            visible=False, 
            content=ft.Column(
                controls=[
                    ft.Text("Calculation History", color=ft.Colors.WHITE, size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(color=ft.Colors.WHITE24),
                    self.history_list
                ]
            )
        )

   
        self.content = ft.Column(
            controls=[
             
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Container(width=40), 
                        ft.IconButton(
                            icon=ft.Icons.HISTORY, 
                            icon_color=ft.Colors.ORANGE,
                            tooltip="Show/Hide History",
                            on_click=self.toggle_history
                        )
                    ]
                ),
                
                ft.Row(controls=[self.expression_display], alignment=ft.MainAxisAlignment.END),
                ft.Row(controls=[self.result], alignment=ft.MainAxisAlignment.END),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                
                
                self.keypad_container,
                self.history_container
            ]
        )

    def toggle_history(self, e):
        is_history_visible = self.history_container.visible
        self.history_container.visible = not is_history_visible
        self.keypad_container.visible = is_history_visible
        
        e.control.icon = ft.Icons.CALCULATE if not is_history_visible else ft.Icons.HISTORY
        self.update()

    def add_history_entry(self, expression, result):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        item = HistoryItem(
            index=self.history_counter,
            timestamp=now,
            expression=expression,
            result=result,
            on_delete=self.delete_history_item
        )
        
        self.history_list.controls.insert(0, item)
        self.history_counter += 1
        
        if len(self.history_list.controls) > 10:
            self.history_list.controls.pop()

    def delete_history_item(self, task):
        self.history_list.controls.remove(task)
        self.update()

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
        
        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            clean_current = str(self.result.value).replace(" ", "")
            if clean_current == "0" or self.new_operand:
                clean_current = data
                self.new_operand = False
            else:
                clean_current = clean_current + data
            self.result.value = self.format_thousands(clean_current)

        elif data in ("sin", "cos", "tan", "√"):
            func_map = {"√": "sqrt"}
            func_name = func_map.get(data, data)
            self.current_expression += f"{func_name}("
            self.expression_display.value = self.current_expression
            self.new_operand = True

        elif data in ("(", ")"):
            clean_current = str(self.result.value).replace(" ", "")
            if data == "(":
                self.current_expression += "("
                self.new_operand = True
            elif data == ")":
                if self.current_expression.endswith(")"):
                     self.current_expression += ")"
                else:
                     self.current_expression += clean_current + ")"
                self.new_operand = True
            self.expression_display.value = self.current_expression

        elif data in ("+", "-", "*", "/"):
            clean_current = str(self.result.value).replace(" ", "")
            if self.current_expression.endswith(")"):
                self.current_expression += data
            else:
                self.current_expression += clean_current + data
            self.expression_display.value = self.current_expression
            self.new_operand = True 

        elif data == "=":
            clean_current = str(self.result.value).replace(" ", "")
            if self.current_expression.endswith(")"):
                final_expression = self.current_expression
            else:
                final_expression = self.current_expression + clean_current
            
            open_count = final_expression.count("(")
            close_count = final_expression.count(")")
            final_expression += ")" * (open_count - close_count)
            
            self.expression_display.value = final_expression + "="
            self.calculate_result(final_expression)
            
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
            formatted_result = self.format_thousands(final_val)
            
           
            self.add_history_entry(expression, formatted_result)
            
            self.result.value = formatted_result
            
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
    page.title = "Scientific Calc with History"
    page.bgcolor = ft.Colors.BLACK
    page.scroll = "adaptive"
    
    calc = CalculatorApp()
    page.add(calc)

ft.run(main)