public class Assessment {
    // instance variables
    public static enum AssessmentNameEnum {MID_TERM_TEST, CODING_TASKS, ESSAY_REPORT, FINAL_EXAM};

    private AssessmentNameEnum assessmentName;
    private double assessmentValue;


    // getter/accessor methods
    public AssessmentNameEnum getAssessmentName(){
        return assessmentName;
    }

    public double getAssessmentValue(){
        return assessmentValue;
    }

    // setter/mutator methods
    public boolean setAssessmentName(AssessmentNameEnum newAssessmentName){
        boolean flag = false;
        assessmentName = newAssessmentName;
        flag = true;
        return flag;
    }

    public boolean setAssessmentValue(double newAssessmentValue){
        boolean flag = false;
        if(newAssessmentValue >= 0 && newAssessmentValue <= 100){
            assessmentValue = newAssessmentValue;
            flag = true;
        } // end of if
        return flag;
    }
}

