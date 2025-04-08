module com.example.apipogoda2 {
    requires javafx.controls;
    requires javafx.fxml;
    requires org.json;

    opens com.example.apipogoda2 to javafx.fxml;
    exports com.example.apipogoda2;
}