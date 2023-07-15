import java.util.Arrays;

public class UnitDriver {

    // Code Task 7 here
    public static void main(String[] args) {
        System.out.println("=======Successful Attempt========");
        //All init parameters pass the guardian code, so the values inputted will be correctly displayed.
        Unit unit1 = new Unit("FIT1051", 6, "Faculty of IT");
        unit1.setOfferedThisSemester(true);
        System.out.println(unit1);

        System.out.println("=======Unsuccessful Attempt=======");
        //The init parameters of unit code and credit hour do not pass the guardian code, so they will be set to default values (0 for int, null for String).
        //However, since the init parameter of offer faculty passes the guardian code, it will be correctly displayed.
        Unit unit2 = new Unit("FIT123456789", -2, "FIT");
        System.out.println(unit2);

        System.out.println("=======Unsuccessful Attempt=======");
        //The init parameter of offer faculty do not pass the guardian code, so it will be set to default value (null for String).
        //Since the init parameter of unit code starts with FIT and the credit hour is not 6, it will be set to default value (0 for int) as it doesn't pass the guardian code.
        //However, since the init parameter of unit code is valid, it will be correctly displayed.
        Unit unit3 = new Unit("FIT1234", 12, "Faculty of Information Technology");
        System.out.println(unit3);

        Unit u = new UnitAssessment("unit", 6, "faculty", new Assessment());

        int[] arr = {1,2,3};
        String str = "MK";
        System.out.println(Arrays.toString(arr) + str);

        //Testing getters
//        System.out.println(unit1.getCreditHour());
//        System.out.println(unit1.getUnitCode());
//        System.out.println(unit1.getUnitName());
//        System.out.println(unit1.getOfferFaculty());
//        System.out.println(unit1.getOfferedThisSemester());

        //Testing setters
//        System.out.println("Expected true get: " + unit1.setUnitCode("FIT9999"));
//        System.out.println("Expected false get: " + unit1.setUnitCode("ABC123456789"));
//        System.out.println("Expected true get: " + unit1.setUnitName("A good unit"));
//        System.out.println("Expected false get: " + unit1.setUnitName("FFFFFFFFFFIIIIIIIIIITTTTTTTTTT12345678901"));
//        System.out.println("Expected true get: " + unit1.setCreditHour(6));
//        System.out.println("Expected false get: " + unit1.setCreditHour(-4));
//        System.out.println("Expected true get: " + unit1.setOfferFaculty("FIT"));
//        System.out.println("Expected false get: " + unit1.setUnitCode("Faculty of Information about Technology"));
//        System.out.println("Expected true get: " + unit1.setOfferedThisSemester(false));



        //Testing customCreditHour
//        Unit unitTest = new Unit("FIT1234" ,6, "FIT" );
//        System.out.println(unitTest.customCreditHour("FIT9999",6));
//        System.out.println(unitTest.customCreditHour("FIT9999",12)); // Unsuccessful attempt
//        System.out.println(unitTest.customCreditHour("ABC1234",6)); //Unsuccessful attempt
//        System.out.println(unitTest.customCreditHour("ABC1234",12));

    }
}
