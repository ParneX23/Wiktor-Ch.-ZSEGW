module com.example.ziptofile {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.example.ziptofile to javafx.fxml;
    exports com.example.ziptofile;
}