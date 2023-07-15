/*
 * Assessment 2
 *
 * Copyright (c) 2022  Monash University
 *
 * Written by  Jonny Low
 *
 *
 */
import java.util.Scanner;

public class Assessment2 {
    public static void main(String[] args){

        Assessment2 a2 = new Assessment2();

        // Instruction: To run your respective task, uncomment below individually
//        a2.task1();
//        a2.task2();
//        a2.task3();
//        a2.task4();

//        test your task 5 here
        Assessment2 obj = new Assessment2();
        obj.pythagorasTheorem(4,5);


    }

    private void task1(){
        // code your task 1 here
        int n;
        boolean testNum;
        //test cases 1-3 (boundary)
        // This checks for the lower boundary.
        n = 0;
        testNum = (n>=1 && n<=100 && ((n<40 || n>50) || (n%2 != 0)));
        System.out.println("n :" + n + " expect false get " + testNum);
        n = 1;
        testNum = (n>=1 && n<=100 && ((n<40 || n>50) || (n%2 != 0)));
        System.out.println("n :" + n + " expect true get " + testNum);
        n = 2;
        testNum = (n>=1 && n<=100 && ((n<40 || n>50) || (n%2 != 0)));
        System.out.println("n :" + n + " expect true get " + testNum);
        // test case 4-6 (boundary)
        // This checks for the upper boundary.
        n = 99;
        testNum = (n>=1 && n<=100 && ((n<40 || n>50) || (n%2 != 0)));
        System.out.println("n :" + n + " expect true get " + testNum);
        n = 100;
        testNum = (n>=1 && n<=100 && ((n<40 || n>50) || (n%2 != 0)));
        System.out.println("n :" + n + " expect true get " + testNum);
        n = 101;
        testNum = (n>=1 && n<=100 && ((n<40 || n>50) || (n%2 != 0)));
        System.out.println("n :" + n + " expect false get " + testNum);
        // test case 7 (scope)
        // This tests for numbers within 1 to 100, but not within 40 to 50.
        n = 39;
        testNum = (n>=1 && n<=100 && ((n<40 || n>50) || (n%2 != 0)));
        System.out.println("n :" + n + " expect true get " + testNum);
        // test case 8 (specific)
        // This tests for odd numbers within 40 to 50.
        n = 45;
        testNum = (n>=1 && n<=100 && ((n<40 || n>50) || (n%2 != 0)));
        System.out.println("n :" + n + " expect true get " + testNum);
        // test case 9 (specific)
        // This tests for even numbers within 40 to 50.
        n = 46;
        testNum = (n>=1 && n<=100 && ((n<40 || n>50) || (n%2 != 0)));
        System.out.println("n :" + n + " expect false get " + testNum);
        // test case 10 (extreme)
        // This tests for negative numbers outside the scope.
        n = -32;
        testNum = (n>=1 && n<=100 && ((n<40 || n>50) || (n%2 != 0)));
        System.out.println("n :" + n + " expect false get " + testNum);
        // test case 11 (extreme)
        // This tests for positive numbers outside the scope.
        n = 169;
        testNum = (n>=1 && n<=100 && ((n<40 || n>50) || (n%2 != 0)));
        System.out.println("n :" + n + " expect false get " + testNum);

    }

    private void task2(){
        // code your task 2 here
        boolean trueVar = true;
        boolean falseVar = false;
        boolean temp;
        System.out.println("Variable 1 before swap: " + trueVar);
        System.out.println("Variable 2 before swap: " + falseVar);
        temp = trueVar;
        trueVar = falseVar;
        falseVar = temp;
        System.out.println("Variable 1 after swap: " + trueVar);
        System.out.println("Variable 2 after swap: " + falseVar);

    }

    private void task3(){
        final double ALPHA = 53.13;
        final double BETA = 41.00;
        final double HEIGHT = 20.00;
        double area;
        double length;
        double width;
        int stoneSlabsRequired;
        int stoneSlabArea = 1;
        width = HEIGHT/Math.tan(ALPHA/180*Math.PI);
        length = HEIGHT/Math.tan(BETA/180*Math.PI);
        area = Math.ceil(width*length);
        stoneSlabsRequired = (int)area/stoneSlabArea;
        System.out.println("The number of stone slabs required is " + stoneSlabsRequired);


    }

    private void task4(){
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter the value for x: ");
        int x = sc.nextInt();
        System.out.println("Enter the value for y: ");
        int y = sc.nextInt();
        System.out.println("The result for bitwise and is: " + (x&y));
        /*x and y are first converted into binary form, then their individual bits are passed through the AND operator. The AND operator returns 1 if both bits are 1,
        otherwise 0. For example, x=1 and y=5, x is 001 and y is 101 in binary, so the result of bitwise AND is 001, thus the result will output 1. */
        System.out.println("The result for bitwise or is: " + (x^y));
        /*x and y are first converted into binary form, then their individual bits are passed through the XOR operator. The XOR operator returns 0 if both bits are the
        same, otherwise 1. For example, x=1 and y=5, x is 001 and y is 101 in binary, so the result of bitwise OR is 100, thus the result will output 4. */
    }

    // Code your task 5 method here
    private double pythagorasTheorem(double a, double b){
        double cNum = Math.sqrt(Math.pow(a,2) + Math.pow(b,2));
        System.out.println("The result of Pythagoras Theorem is: " + cNum);
        return cNum;
    }


}

