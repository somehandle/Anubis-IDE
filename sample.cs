/*
 * C# Program to Perform Celsius to Fahrenheit Conversion
 */
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
 
namespace program
{
    class Program
    {
        static void Main(string[] args)
        {
            int celsius, faren;
            Console.WriteLine("Enter the Temperature in Celsius(°C) : ");
            celsius = int.Parse(Console.ReadLine());
            faren = (celsius * 9) / 5 + 32;
            Console.WriteLine("0Temperature in Fahrenheit is(°F) : " + faren);
            Console.ReadLine();
 
        }
    }
}
