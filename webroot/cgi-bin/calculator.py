#!/usr/bin/env python3

import cgi
import cgitb

cgitb.enable()

form = cgi.FieldStorage()
num1 = form.getvalue('num1')
num2 = form.getvalue('num2')
operation = form.getvalue('operation')

print("Content-Type: text/html")
print()

if num1 is None or num2 is None or operation not in ['sum', 'product']:
    print("<html><body><h1>Invalid Input</h1>")
    print(f"<p>num1: {num1}, num2: {num2}, operation: {operation}</p>")
    print("</body></html>")
else:
    num1 = float(num1)
    num2 = float(num2)
    if operation == 'sum':
        result = num1 + num2
        op_str = 'Sum'
    else:
        result = num1 * num2
        op_str = 'Product'

    print(f"<html><body><h1>{op_str} of {num1} and {num2} is {result}</h1>")
    print(f"<p>num1: {num1}, num2: {num2}, operation: {operation}</p>")
    print("</body></html>")
