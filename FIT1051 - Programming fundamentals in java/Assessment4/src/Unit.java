public class Unit {

    // Task 1: Instance Variables
    private int creditHour;
    private String offerFaculty;
    private boolean offeredThisSemester;
    private String unitCode;
    private String unitName;


    // Task 2: constructors
    //default constructor for the use of UnitAssessment class.
    public Unit(){
        setUnitCode(null);

        setUnitName(null);

        setCreditHour(0);

        setOfferFaculty(null);

        setOfferedThisSemester(false);
    }

    public Unit(String initUnitCode, int initCreditHour, String initOfferFaculty){
        setUnitCode(initUnitCode);

        setUnitName("Not yet given"); //default value

        setCreditHour(initCreditHour);

        setOfferFaculty(initOfferFaculty);

        setOfferedThisSemester(false); //default value
    }

    // Task 3: Getter
    public int getCreditHour(){
        return creditHour;
    }

    public String getOfferFaculty(){
        return offerFaculty;
    }

    public boolean getOfferedThisSemester(){
        return offeredThisSemester;
    }

    public String getUnitCode(){
        return unitCode;
    }

    public String getUnitName(){
        return unitName;
    }



    // Task 4: Setter
    public boolean setCreditHour(int newCreditHour){
        boolean flag = false;
        if(newCreditHour == 6){
            creditHour = newCreditHour;
            flag = true;
        }

        return flag;
    }

    public boolean setOfferFaculty(String newOfferFaculty){
        boolean flag = false;
        if(newOfferFaculty.length() <= 20){
            offerFaculty = newOfferFaculty;
            flag = true;
        }
        return flag;
    }

    public boolean setOfferedThisSemester(boolean newOfferedThisSemester){
        boolean flag = false;
        offeredThisSemester = newOfferedThisSemester;
        flag = true;
        return flag;
    }

    public boolean setUnitCode(String newUnitCode){
        boolean flag = false;
        if(newUnitCode.length() <= 7){
            unitCode = newUnitCode;
            flag = true;
        }
        return flag;
    }

    public boolean setUnitName(String newUnitName){
        boolean flag = false;
        if(newUnitName.length() <= 40){
            unitName = newUnitName;
            flag = true;
        }
        return flag;
    }



    // Task 5: toString method
    public String toString(){
        String retStr = "";
        retStr += "Unit Code: " + getUnitCode() + "\n";
        retStr += "Offered Faculty: " + getOfferFaculty() + "\n";
        retStr += "Credit Hour: " + getCreditHour() + "\n";
        retStr += "Offered in this Semester? : " + getOfferedThisSemester() + "\n";

        return retStr;
    }

    // Task 6: customCreditHour method
    public String customCreditHour(String customUnitCode, int customCreditHour){
        String retStr = "";
        if((customUnitCode.charAt(0) == 'F') && (customUnitCode.charAt(1) == 'I') && (customUnitCode.charAt(2) == 'T')){
            if (customCreditHour != 6) {
                retStr = "Error. This is FIT unit and the no of credit hours is 6 by default.";
            }
            else{
                unitCode = customUnitCode;
                creditHour = customCreditHour;
                retStr = "Success. The unit is: " + customUnitCode + " and its number of credit hours is " + customCreditHour;
            }
        }
        else{
            unitCode = customUnitCode;
            creditHour = customCreditHour;
            retStr = "Success. The unit is: " + customUnitCode + " and its number of credit hours is " + customCreditHour;

        }

        return retStr;
    }
}
