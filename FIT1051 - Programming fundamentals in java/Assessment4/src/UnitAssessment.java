import java.util.ArrayList;
public class UnitAssessment extends Unit{
    // instance variables
    private ArrayList<Assessment> assessmentList;
    private Assessment typeOfAssessment;

    // constructor
    public UnitAssessment(String initUnitCode, int initCreditHour, String initOfferFaculty, Assessment initTypeOfAssessment){
        super(initUnitCode, initCreditHour, initOfferFaculty);
        typeOfAssessment = initTypeOfAssessment;
        assessmentList = new ArrayList<Assessment>();
        addAssessment(typeOfAssessment);
    }

    // public method
    public boolean addAssessment(Assessment newAssessment){
        boolean flag = false;
        if(assessmentList.size() <= 10){
            assessmentList.add(newAssessment);
            flag=  true;
        }
        return flag;
    }


}


