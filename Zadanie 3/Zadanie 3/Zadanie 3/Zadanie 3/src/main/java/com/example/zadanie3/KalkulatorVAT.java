package com.example.zadanie3;

import javafx.application.Application;
import javafx.collections.ObservableList;
import javafx.event.EventHandler;
import javafx.fxml.FXMLLoader;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.input.MouseEvent;
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
        oslist.addAll("04%","05%","07%","08%","23%");

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

        ButtonBar przyciski = new ButtonBar();
        Button oblicz = new Button("OBLICZ");
        Button zamknij = new Button("Zamknij");

        przyciski.getButtons().addAll(oblicz, zamknij);

        Label wynikiLabel = new Label();
        wynikiLabel.setGraphic(new Label(" Wyniki: "));
        wynikiLabel.setPadding(new Insets(-30, -10, 0, 0));
        wynikiLabel.getGraphic().setStyle("-fx-background-color: #f4f4f4;");

        Label NettoLabel = new Label("Netto:");
        Label VATLabel = new Label("VAT:");
        Label BruttoLabel = new Label("Brutto");

        Label NettoValueLabel = new Label("0,00");
        Label VATValueLabel = new Label("0,00");
        Label VATProcLabel = new Label("0%");
        Label BruttoValueLabel = new Label("0,00");

        GridPane wynikiPane = new GridPane();
        wynikiPane.setVgap(5);
        wynikiPane.setHgap(5);
        wynikiPane.setPadding(new Insets(15));
        wynikiPane.add(wynikiLabel, 0, 0);
        wynikiPane.add(NettoLabel, 0, 1);
        wynikiPane.add(VATLabel, 0, 2);
        wynikiPane.add(BruttoLabel, 0, 3);
        wynikiPane.add(NettoValueLabel, 1, 1);
        wynikiPane.add(VATValueLabel, 1, 2);
        wynikiPane.add(VATProcLabel, 2, 2);
        wynikiPane.add(BruttoValueLabel, 1, 3);
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
        main.add(przyciski, 0, 2);
        main.add(wynikiPane, 0, 3);

        oblicz.setOnMouseClicked((new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent mouseEvent) {
                System.out.println(MetodaObliczen.getSelectedToggle().getProperties());
                if (MetodaObliczen.getSelectedToggle().getProperties().toString().substring(33,34).equals("1")){
                    NettoValueLabel.setText(wartosc.getText());
                    VATValueLabel.setText(String.valueOf((Double.parseDouble(vat.getValue().toString().substring(0,2))*Double.parseDouble(wartosc.getText()))/100.00));
                    VATProcLabel.setText(vat.getValue());
                    BruttoValueLabel.setText(String.valueOf(Double.parseDouble(NettoValueLabel.getText())-Double.parseDouble(VATValueLabel.getText())));
                } else if (MetodaObliczen.getSelectedToggle().getProperties().toString().substring(33,34).equals("2")){
                    BruttoValueLabel.setText(wartosc.getText());
                    VATValueLabel.setText(String.valueOf(Double.parseDouble(NettoValueLabel.getText())-Double.parseDouble(BruttoValueLabel.getText())));
                    VATProcLabel.setText(vat.getValue());
                    NettoValueLabel.setText(String.valueOf((Double.parseDouble(BruttoValueLabel.getText())*100.00)/(100.00-Double.parseDouble(vat.getValue().toString().substring(0,2)))));
                } else if (MetodaObliczen.getSelectedToggle().getProperties().toString().substring(33,34).equals("3")){
                    VATValueLabel.setText(wartosc.getText());
                    VATProcLabel.setText(vat.getValue());
                    NettoValueLabel.setText(String.valueOf((Double.parseDouble(VATValueLabel.getText())*100.00)/Double.parseDouble(vat.getValue().toString().substring(0,2))));
                    BruttoValueLabel.setText(String.valueOf(Double.parseDouble(NettoValueLabel.getText())-Double.parseDouble(VATValueLabel.getText())));
                } else System.out.println("nie wybrano metody");
            }
        }));

        Scene scene = new Scene(main, 300, 400);
        stage.setTitle("Kalkulator VAT netto-brutto");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}