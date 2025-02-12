package com.example.ziptofile;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.layout.GridPane;
import javafx.stage.Stage;

import java.io.IOException;

public class HelloApplication extends Application {
    @Override
    public void start(Stage stage) throws IOException {
        GridPane main = new GridPane();



        Scene scene = new Scene(main, 320, 240);
        stage.setTitle("ZipToFile");
        stage.setScene(scene);
        stage.show();
    }
}