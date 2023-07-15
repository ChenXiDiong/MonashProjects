/*
 * Assessment 3
 *
 * Copyright (c) 2022  Monash University
 *
 * Written by  Jonny Low
 *
 *
 */
import java.lang.reflect.Array;
import java.util.Arrays;
import java.util.ArrayList;
public class Assessment3 {

    public static void main(String[] args){

        Assessment3 a3 = new Assessment3();

        // Instruction: To run your respective task, uncomment below individually
//        a3.task1a();
//        a3.task2();
//        a3.task3();
//        a3.gradeScale("80");
//        a3.daysOfTheWeek("2");
//        a3.task6();
//        a3.task7();


    }


    private void task1a(){
        double[] doubleArray = {1.23, 2.34, 3.45, 4.56, 5.67};
        System.out.println("The Value Type before method call is: " + doubleArray[4]);
        System.out.println("The Reference Type before method call is: " + Arrays.toString(doubleArray));
        task1b(doubleArray, doubleArray[4]);
        /* Value Type does not have side effects as a copy of it is created during the method call and the original item
        passed into the method remains unchanged. */
        System.out.println("The Value Type after method call is: " + doubleArray[4]); //No side effect
        /* Reference Type is merely a pointer towards an address, so if an array is passed into a method and the method
        alters the items inside the array, side effects will occur and the array's items on the caller's side would be
        changed as well. */
        System.out.println("The Reference Type after method call is: " + Arrays.toString(doubleArray)); //Side effect occurs.
    }

    private void task1b(double[] someArray, double someDouble){
        someArray[1]++;
        someDouble++;
        System.out.println("The Value Type during method call is: " + someDouble);
        //Here the copy of the Value Type is changed only
        System.out.println("The Reference Type during method call is: " + Arrays.toString(someArray));
        //Here the value that the Reference Type is pointing to is changed

    }

    private void task2(){
        int firstVar=1, secondVar=10, thirdVar=100, fourthVar=1000;
        String resStr = String.format("%8d\n" + "%8d\n" + "%8d\n" + "%8d", firstVar, secondVar, thirdVar, fourthVar);
        System.out.println(resStr);

    }

    private void task3(){
        //Declare an array list named myList which has the capacity of 10.
        ArrayList<String> myList = new ArrayList<>(10);
        //Add the following numbers: "one", "seven", "five", "three", "eight", "ten".
        myList.add("one");
        myList.add("seven");
        myList.add("five");
        myList.add("three");
        myList.add("eight");
        myList.add("ten");
        //Insert the value "eleven" in between "five" and "three", which is in index 3.
        myList.add(3,"eleven");
        //Print all the elements in the myList
        System.out.println(myList);
        //Delete the second last element in the myList, total # of elements = 7, index of second last element is 5.
        myList.remove(5);
        //Print true if myList contains "seven"; false otherwise.
        System.out.println(myList.contains("seven"));


    }

    private String gradeScale(String mark){
        String grade;
        int intMark = Integer.parseInt(mark);
        if (intMark >= 80 && intMark <= 100){
            grade = "High Distinction";
        }
        else if (intMark >= 70 && intMark <= 79){
            grade = "Distinction";
        }
        else if (intMark >= 60 && intMark <= 69){
            grade = "Credit";
        }
        else if (intMark >= 50 && intMark <= 59){
            grade = "Pass";
        }
        else if (intMark >= 0 && intMark <= 49){
            grade = "Fail";
        }
        else{
            grade = "Invalid marks!";
        }
        System.out.println(grade);
        return grade;
    }

    private String daysOfTheWeek(String day){
        String result;
        switch(day){
            case "1":
                result = "Monday";
                break;
            case "2":
                result = "Tuesday";
                break;
            case "3":
                result = "Wednesday";
                break;
            case "4":
                result = "Thursday";
                break;
            case "5":
                result = "Friday";
                break;
            case "6":
                result = "Saturday";
                break;
            case "7":
                result = "Sunday";
                break;
            default:
                result = "Invalid day!";
                break;
        }
        System.out.println(result);
        return result;
    }


    private void task6(){
        int radiusOfCircle = 1;
        double circumferenceOfCircle = 2 * Math.PI * radiusOfCircle;
        double areaOfCircle = Math.PI * Math.pow(radiusOfCircle, 2);
        double ratioOfAreaToCircumference = areaOfCircle / circumferenceOfCircle;

        while(ratioOfAreaToCircumference < 30){
            System.out.println("The radius of the circle is: " + radiusOfCircle);
            System.out.println("The ratio of area to circumference is:" + ratioOfAreaToCircumference);
            radiusOfCircle++;
            circumferenceOfCircle = 2 * Math.PI * radiusOfCircle;
            areaOfCircle = Math.PI * Math.pow(radiusOfCircle, 2);
            ratioOfAreaToCircumference = areaOfCircle / circumferenceOfCircle;
        };


    }


    private void task7(){
        int size = 7;
        int i, j;
        String s = "";
        for(i=0; i<size; i++){
            s = "";
            for(j=0; j<size; j++){
                if(i==j){
                    s += "*";
                }
                else if ((i+j) == (size-1)){
                    s += "*";
                }
                else{
                    s += " ";
                }
            }
            System.out.println(s);
        }


    }





}

