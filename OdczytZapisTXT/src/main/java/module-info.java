module com.example.odczytzapistxt {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.example.odczytzapistxt to javafx.fxml;
    exports com.example.odczytzapistxt;
}