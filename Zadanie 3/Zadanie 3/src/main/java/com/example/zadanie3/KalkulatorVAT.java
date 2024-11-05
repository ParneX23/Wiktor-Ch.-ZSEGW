package com.example.zadanie3;

import javafx.application.Application;
import javafx.collections.ObservableList;
import javafx.fxml.FXMLLoader;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.Border;
import javafx.scene.layout.GridPane;
import javafx.stage.Stage;

import java.io.IOException;

public class KalkulatorVAT extends Application {
    @Override
    public void start(Stage stage) throws IOException {
        RadioButton ONDB = new RadioButton("Od netto do brutto");
        RadioButton OBDN = new RadioButton("Od brutto do netto");
        RadioButton VAT = new RadioButton("Dopasuj do kwoty VAT");

        Label metodaLabel = new Label();
        metodaLabel.setGraphic(new Label(" Metoda obliczeń: "));
        metodaLabel.setPadding(new Insets(-30, -10, 0, 0));
        metodaLabel.getGraphic().setStyle("-fx-background-color: #f4f4f4;");

        GridPane metodaPane = new GridPane();
        metodaPane.setVgap(5);
        metodaPane.setHgap(5);
        metodaPane.setPadding(new Insets(15));
        //metodaPane.setLayoutX(100);
        //metodaPane.setLayoutY(100);
        metodaPane.add(metodaLabel, 0, 0);
        metodaPane.add(ONDB, 0, 1);
        metodaPane.add(OBDN, 0, 2);
        metodaPane.add(VAT, 0, 3);
        metodaPane.setStyle("-fx-border-style: solid inside;");
        metodaPane.setStyle("-fx-border-width: 1;");
        metodaPane.setStyle("-fx-border-insets: 1;");
        metodaPane.setStyle("-fx-border-radius: 1;");
        metodaPane.setStyle("-fx-border-color: gray;");

        ToggleGroup MetodaObliczen = new ToggleGroup();
        ONDB.setToggleGroup(MetodaObliczen);
        OBDN.setToggleGroup(MetodaObliczen);
        VAT.setToggleGroup(MetodaObliczen);


        Label daneLabel = new Label();
        daneLabel.setGraphic(new Label(" Dane: "));
        daneLabel.setPadding(new Insets(-30, -10, 0, 0));
        daneLabel.getGraphic().setStyle("-fx-background-color: #f4f4f4;");

        Label wartoscLabel = new Label("Wartość bazowa:");

        TextField wartosc = new TextField();


        Label vatLabel = new Label("Stawka VAT:");

        ChoiceBox<String> vat = new ChoiceBox<String>();
        ObservableList<String> oslist = vat.getItems();
        oslist.addAll("4%","5%","7%","8%","23%");

        GridPane danePane = new GridPane();
        danePane.setVgap(5);
        danePane.setHgap(5);
        danePane.setPadding(new Insets(15));
        danePane.add(daneLabel, 0, 0);
        danePane.add(wartoscLabel, 0, 1);
        danePane.add(wartosc, 1, 1);
        danePane.add(vatLabel, 0, 2);
        danePane.add(vat, 1, 2);
        danePane.setStyle("-fx-border-style: solid inside;");
        danePane.setStyle("-fx-border-width: 1;");
        danePane.setStyle("-fx-border-insets: 1;");
        danePane.setStyle("-fx-border-radius: 1;");
        danePane.setStyle("-fx-border-color: gray;");



        Label wynikiLabel = new Label();
        wynikiLabel.setGraphic(new Label(" Wyniki: "));
        wynikiLabel.setPadding(new Insets(-30, -10, 0, 0));
        wynikiLabel.getGraphic().setStyle("-fx-background-color: #f4f4f4;");

        GridPane wynikiPane = new GridPane();
        wynikiPane.setVgap(5);
        wynikiPane.setHgap(5);
        wynikiPane.setPadding(new Insets(15));
        wynikiPane.add(wynikiLabel, 0, 0);
        wynikiPane.setStyle("-fx-border-style: solid inside;");
        wynikiPane.setStyle("-fx-border-width: 1;");
        wynikiPane.setStyle("-fx-border-insets: 1;");
        wynikiPane.setStyle("-fx-border-radius: 1;");
        wynikiPane.setStyle("-fx-border-color: gray;");

        GridPane main = new GridPane();
        main.setPadding(new Insets(10,10,10,10));
        main.setMinSize(500, 300);
        main.setAlignment(Pos.TOP_CENTER);
        main.setVgap(5);
        main.setHgap(5);

        main.add(metodaPane, 0,0);
        main.add(danePane, 0, 1);
        main.add(wynikiPane, 0, 2);

        Scene scene = new Scene(main, 500, 300);
        stage.setTitle("Kalkulator VAT netto-brutto");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}