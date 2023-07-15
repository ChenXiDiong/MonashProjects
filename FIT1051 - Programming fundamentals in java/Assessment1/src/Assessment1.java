/*
 * Week 03 Assessment Solution (3%)
 *
 * Copyright (c) 2022  Monash University
 *
 * Written by  Jonny Low
 *
 *
 */



public class Assessment1 {

    public static void main(String[] args){

        Assessment1 a1 = new Assessment1();

        // Instruction: To run your respective task, uncomment below individually
        //a1.task1();
        //a1.task2();
        //a1.task3();
        //a1.task4();
        //a1.task5();

    }

    private void task1(){
        // Without using variables
        System.out.println(5);
        System.out.println(8);
        System.out.println(4);
        System.out.println(2);
        System.out.println(5+8+4+2);

        //Using 4 independent variables
        int firstNum = 5;
        int secondNum = 8;
        int thirdNum = 4;
        int fourthNum = 2;
        int sum = firstNum + secondNum + thirdNum + fourthNum;
        System.out.println(firstNum);
        System.out.println(secondNum);
        System.out.println(thirdNum);
        System.out.println(fourthNum);
        System.out.println(sum);

        //Reusing one variable
        int newSum = 0;
        int num = 5;
        newSum += num;
        System.out.println(num);
        num = 8;
        newSum += num;
        System.out.println(num);
        num = 4;
        newSum += num;
        System.out.println(num);
        num = 2;
        newSum += num;
        System.out.println(num);
        System.out.println(newSum);

    }

    private void task2(){
        int joggingSpeed = 5;
        String lecturerName = "Lim Mei Kuan";
        int passengerCapacity = 2000;
        int deskLength = 960;
        boolean lightState = Boolean.TRUE;
        int bookCount = 300;
        int vaccinationAmount = 3;
        int currentTemperature = 27;
        int aceNum = 4;
        int memorySize = 512;
        String trafficLight = "RED";
        System.out.println("Your jogging speed: " + joggingSpeed + "mph");
        System.out.println("Name of FIT1051 lecturer: " + lecturerName);
        System.out.println("Capacity of passengers in train wagon: " + passengerCapacity + " people");
        System.out.println("Length of desk: " + deskLength + "mm");
        System.out.println("State of light switch: " + lightState);
        System.out.println("Number of books on library shelf: " + bookCount + " books");
        System.out.println("Amount of COVID vaccinations a person can have: " + vaccinationAmount + " shots");
        System.out.println("Current temperature of the day: " + currentTemperature + " degrees Celsius");
        System.out.println("Number of Aces in a deck of cards: " + aceNum);
        System.out.println("Memory size of computer chip: " + memorySize + "Gb");
        System.out.println("State of traffic light: " + trafficLight);


    }

    private void task3(){
        float floatNum = 4.3f;
        int intNum = 6;
        String someString = "Hello";
        double doubleNum = 3.14;
        boolean bool = Boolean.TRUE;
        floatNum = intNum;
        // floatNum = someString;
        floatNum = (float)doubleNum;
        // floatNum = bool;
        intNum = (int)floatNum;
        // intNum = someString;
        intNum = (int)doubleNum;
        // intNum = bool;
        // someString = floatNum;
        // someString = intNum;
        // someString = doubleNum;
        // someString = bool;
        doubleNum = floatNum;
        doubleNum = intNum;
        // doubleNum = someString;
        // doubleNum = bool;
        // bool = floatNum;
        // bool = intNum;
        // bool = someString;
        // bool = doubleNum;

        // Q1 : Java converts integers to floats or doubles, and floats to doubles automatically (widening conversion).
        /* Q2 : Java converts doubles to integers or floats, and floats to integers with a cast (narrowing conversion). The side
        effect is casting may cause the original values to have some information loss during the conversion. */
    }

    private void task4(){
        String lineOne = "             @@@@@@@@@@@@@@@@@@@\n";
        String lineTwo = "          @@@@@@@@@@@@@@@@@@@@@@@@\n";
        String lineThree = "        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n";
        String lineFour = "      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n";
        String lineFive = "   @@@@@@@      @@@@@@@@@@@@     @@@@@@@\n";
        String lineSix = "  @@@@@@@        @@@@@@@@@@       @@@@@@@@\n";
        String lineSeven = "@@@@@@@@@@      @@@@@@@@@@@      @@@@@@@@@@\n";
        String lineEight = "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n";
        String lineNine = "  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n";
        String lineTen = "   @@@@@@@@@@   @@@@@@@@@@   @@@@@@@@@@\n";
        String lineEleven = "    @@@@@@@@@@  @@@@@@@@@@  @@@@@@@@@@\n";
        String lineTwelve = "     @@@@@@@@@@            @@@@@@@@@@\n";
        String lineThirteen = "       @@@@@@@@@@@@@@@@@@@@@@@@@@@@\n";
        String lineFourteen = "          @@@@@@@@@@@@@@@@@@@@@@\n";
        String lineFifteen = "            @@@@@@@@@@@@@@@@@@";
        System.out.println(lineOne + lineTwo + lineThree + lineFour + lineFive + lineSix + lineSeven + lineEight + lineNine + lineTen + lineEleven + lineTwelve + lineThirteen + lineFourteen + lineFifteen);
    }

    private void task5(){
        String s = null;
        //System.out.println(s.length());

        // 1. The error is a NullPointerException error. The "String.length()" method cannot be invoked because the string "s" is null.
        /* 2. When the "String.length" method is invoked, it takes in a string and returns its length to the user. But, since the input
        string "s" does not have any location in the memory (i.e. null), the pointer has nothing to point to, thus Java will throw an
        error indicating that a method cannot be invoked on a null reference.
         */
    }


}