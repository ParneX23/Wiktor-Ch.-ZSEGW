module com.example.dbadmin {
    requires javafx.controls;
    requires javafx.fxml;
    requires java.sql;
    requires java.desktop;
    requires jdk.jdi;


    opens com.example.dbadmin to javafx.fxml;
    exports com.example.dbadmin;
}