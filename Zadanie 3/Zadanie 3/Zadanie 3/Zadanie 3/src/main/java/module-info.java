module com.example.zadanie3 {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.example.zadanie3 to javafx.fxml;
    exports com.example.zadanie3;
}